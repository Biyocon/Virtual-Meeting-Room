"""Test sidecar endpoints."""

import asyncio
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import agent_sidecar.main as main_module
from agent_sidecar.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHealth:
    """GET /health."""

    def test_health_ok(self, client):
        """Health check returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["service"] == "agent-sidecar"


class TestAgentRespond:
    """POST /agent/respond."""

    def test_agent_respond_agent_add(self, client):
        """POST /agent/respond accepts agent.add command."""
        payload = {
            "type": "agent.add",
            "scope": {
                "tenantId": "tenant-1",
                "meetingId": "meeting-1",
            },
            "correlationId": "corr-1",
            "payload": {
                "agentProfileId": "profile-1",
                "role": "analyst",
            },
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 202
        assert "correlationId" in response.json()

    def test_agent_respond_agent_respond(self, client):
        """POST /agent/respond accepts agent.respond command."""
        payload = {
            "type": "agent.respond",
            "scope": {
                "tenantId": "tenant-1",
                "meetingId": "meeting-1",
                "agentInstanceId": "agent-1",
            },
            "correlationId": "corr-2",
            "payload": {
                "agentInstanceId": "agent-1",
                "prompt": "What is 2+2?",
            },
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 202
        assert response.json()["correlationId"] == "corr-2"

    def test_agent_respond_invalid_command_type(self, client):
        """POST /agent/respond rejects invalid command type."""
        payload = {
            "type": "invalid.command",
            "scope": {"tenantId": "t1", "meetingId": "m1"},
            "correlationId": "corr-3",
            "payload": {},
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 400

    def test_agent_respond_missing_required_field(self, client):
        """POST /agent/respond rejects commands missing required fields."""
        payload = {
            "type": "agent.respond",
            "scope": {"tenantId": "t1", "meetingId": "m1"},
            "correlationId": "corr-4",
            # Missing payload
            "payload": {},
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 400


def respond_command(meeting_id: str, agent_id: str, corr_id: str) -> dict:
    return {
        "type": "agent.respond",
        "scope": {
            "tenantId": "tenant-test",
            "meetingId": meeting_id,
            "agentInstanceId": agent_id,
        },
        "correlationId": corr_id,
        "payload": {"agentInstanceId": agent_id, "prompt": "ping"},
    }


async def drain_until_idle(
    queue: asyncio.Queue, idle_count: int = 1, timeout: float = 5.0
) -> list[dict]:
    """Collect bus events (as dicts) until N status:idle events seen."""
    events: list[dict] = []
    idle_seen = 0
    async with asyncio.timeout(timeout):
        while idle_seen < idle_count:
            event = (await queue.get()).model_dump()
            events.append(event)
            if (
                event["type"] == "agent.status"
                and event["payload"]["status"] == "idle"
            ):
                idle_seen += 1
    return events


class TestAgentEvents:
    """Command-driven event stream (M2 DoD): respond drives the bus/SSE.

    NOTE: exercised at bus/endpoint-function level — httpx ASGITransport
    buffers full responses, so an open-ended SSE stream can't be consumed
    through it. Real HTTP E2E lands with the BFF proxy test (ticket #2).
    """

    async def test_respond_drives_event_stream(self):
        """POST /agent/respond → thinking→deltas→speaking→final→idle."""
        queue = main_module.bus.subscribe("meeting-e2e")
        try:
            result = await main_module.agent_respond(
                respond_command(
                    "meeting-e2e", "agent-abdi-asis-pm", "corr-e2e"
                )
            )
            assert result == {"correlationId": "corr-e2e"}
            events = await drain_until_idle(queue)
        finally:
            main_module.bus.unsubscribe("meeting-e2e", queue)

        statuses = [
            e["payload"]["status"]
            for e in events
            if e["type"] == "agent.status"
        ]
        assert statuses == ["thinking", "speaking", "idle"]
        assert any(e["type"] == "agent.message.delta" for e in events)
        finals = [e for e in events if e["type"] == "agent.message.final"]
        assert len(finals) == 1
        assert finals[0]["payload"]["text"] == "Hello from Python sidecar"

    async def test_events_carry_command_ids(self):
        """Events use the command's IDs — no generated agent-0/uuid."""
        queue = main_module.bus.subscribe("meeting-ids")
        try:
            await main_module.agent_respond(
                respond_command(
                    "meeting-ids", "agent-abdi-asis-pm", "corr-ids"
                )
            )
            events = await drain_until_idle(queue)
        finally:
            main_module.bus.unsubscribe("meeting-ids", queue)

        assert events, "expected respond-sequence events"
        for event in events:
            assert event["meetingId"] == "meeting-ids"
            assert event["agentInstanceId"] == "agent-abdi-asis-pm"
            assert event["correlationId"] == "corr-ids"

    async def test_two_agents_no_cross_contamination(self):
        """Two commands with distinct instanceIds keep their own sequences."""
        queue = main_module.bus.subscribe("meeting-two")
        try:
            await main_module.agent_respond(
                respond_command("meeting-two", "agent-a", "corr-a")
            )
            await main_module.agent_respond(
                respond_command("meeting-two", "agent-b", "corr-b")
            )
            events = await drain_until_idle(queue, idle_count=2)
        finally:
            main_module.bus.unsubscribe("meeting-two", queue)

        for event in events:
            if event["type"] == "audit.event":
                continue
            expected = (
                "corr-a" if event["agentInstanceId"] == "agent-a" else "corr-b"
            )
            assert event["correlationId"] == expected

    async def test_meeting_scoping_no_leak(self):
        """Subscriber on another meetingId never sees the events."""
        scoped = main_module.bus.subscribe("meeting-scoped")
        other = main_module.bus.subscribe("meeting-other")
        try:
            await main_module.agent_respond(
                respond_command("meeting-scoped", "agent-a", "corr-s")
            )
            await drain_until_idle(scoped)
            assert other.qsize() == 0
        finally:
            main_module.bus.unsubscribe("meeting-scoped", scoped)
            main_module.bus.unsubscribe("meeting-other", other)

    async def test_reconnect_does_not_replay(self):
        """After a completed sequence, a fresh subscriber gets nothing."""
        queue = main_module.bus.subscribe("meeting-replay")
        try:
            await main_module.agent_respond(
                respond_command("meeting-replay", "agent-a", "corr-r")
            )
            await drain_until_idle(queue)
        finally:
            main_module.bus.unsubscribe("meeting-replay", queue)

        fresh = main_module.bus.subscribe("meeting-replay")
        try:
            with pytest.raises(TimeoutError):
                async with asyncio.timeout(0.3):
                    await fresh.get()
        finally:
            main_module.bus.unsubscribe("meeting-replay", fresh)


class TestSSEGenerator:
    """The SSE endpoint's generator: retry directive, data frames, heartbeat."""

    async def test_stream_emits_data_and_heartbeat(self, monkeypatch):
        monkeypatch.setattr(main_module, "HEARTBEAT_SECONDS", 0.2)
        response = await main_module.agent_events_stream("meeting-sse")
        assert response.media_type == "text/event-stream"
        stream = response.body_iterator

        first = await anext(stream)
        assert first.startswith("retry:")

        event = main_module.AgentStatusEvent(
            type="agent.status",
            meetingId="meeting-sse",
            agentInstanceId="agent-a",
            ts="2026-07-02T00:00:00+00:00",
            correlationId="corr-sse",
            payload=main_module.AgentStatusPayload(status="thinking"),
        )
        await main_module.bus.publish("meeting-sse", event)

        async with asyncio.timeout(1.0):
            chunk = await anext(stream)
        assert chunk.startswith("data: ")
        assert json.loads(chunk[6:])["correlationId"] == "corr-sse"

        # No events → heartbeat comment
        async with asyncio.timeout(1.0):
            chunk = await anext(stream)
        assert chunk.startswith(": heartbeat")

        await stream.aclose()
        # aclose runs finally → subscriber removed → publish reaches no one
        await main_module.bus.publish("meeting-sse", event)
