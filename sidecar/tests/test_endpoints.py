"""Test sidecar endpoints."""

import asyncio
import json

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from agent_sidecar.contracts import (
    AgentStatusEvent,
    AgentStatusPayload,
)
from agent_sidecar.main import app
from agent_sidecar.routes import agent as agent_routes
from agent_sidecar.runtime.instance import reset_instances
from agent_sidecar.runtime.profile_loader import reset_profile_cache
from agent_sidecar.runtime.state import (
    HEARTBEAT_SECONDS,
    bus,
    reset_tenant_registry,
)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset all in-memory state between tests."""
    reset_profile_cache()
    reset_tenant_registry()
    reset_instances()
    yield
    reset_profile_cache()
    reset_tenant_registry()
    reset_instances()


@pytest.fixture
def client():
    return TestClient(app)


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
                "agentProfileId": "pm",
                "role": "chair",
            },
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 202
        assert "correlationId" in response.json()

    def test_agent_respond_agent_add_unknown_profile(self, client):
        """POST /agent/respond rejects unknown agentProfileId."""
        payload = {
            "type": "agent.add",
            "scope": {
                "tenantId": "tenant-1",
                "meetingId": "meeting-1",
            },
            "correlationId": "corr-1",
            "payload": {
                "agentProfileId": "does-not-exist",
                "role": "chair",
            },
        }
        response = client.post("/agent/respond", json=payload)
        assert response.status_code == 400

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

    async def test_agent_respond_payload_instance_id_without_scope(self):
        """Regression: payload.agentInstanceId is authoritative when scope field is omitted.

        Contract allows scope.agentInstanceId to be optional, but the respond
        sequence must still attribute events to payload.agentInstanceId.
        """
        queue = bus.subscribe("meeting-payload-only")
        try:
            await agent_routes.agent_respond({
                "type": "agent.respond",
                "scope": {
                    "tenantId": "tenant-1",
                    "meetingId": "meeting-payload-only",
                },
                "correlationId": "corr-payload-only",
                "payload": {
                    "agentInstanceId": "agent-from-payload",
                    "prompt": "Hello?",
                },
            })
            events = await drain_until_idle(queue, timeout=3.0)
        finally:
            bus.unsubscribe("meeting-payload-only", queue)

        finals = [e for e in events if e["type"] == "agent.message.final"]
        assert len(finals) == 1
        assert finals[0]["agentInstanceId"] == "agent-from-payload"
        assert finals[0]["correlationId"] == "corr-payload-only"

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


class TestAgentEvents:
    """Command-driven event stream (M2 DoD): respond drives the bus/SSE."""

    async def test_respond_drives_event_stream(self):
        """POST /agent/respond → thinking→deltas→speaking→final→idle."""
        queue = bus.subscribe("meeting-e2e")
        try:
            result = await agent_routes.agent_respond(
                respond_command("meeting-e2e", "agent-abdi-asis-pm", "corr-e2e")
            )
            assert result == {"correlationId": "corr-e2e"}
            events = await drain_until_idle(queue)
        finally:
            bus.unsubscribe("meeting-e2e", queue)

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
        queue = bus.subscribe("meeting-ids")
        try:
            await agent_routes.agent_respond(
                respond_command("meeting-ids", "agent-abdi-asis-pm", "corr-ids")
            )
            events = await drain_until_idle(queue)
        finally:
            bus.unsubscribe("meeting-ids", queue)

        assert events, "expected respond-sequence events"
        for event in events:
            assert event["meetingId"] == "meeting-ids"
            assert event["agentInstanceId"] == "agent-abdi-asis-pm"
            assert event["correlationId"] == "corr-ids"

    async def test_two_agents_no_cross_contamination(self):
        """Two commands with distinct instanceIds keep their own sequences."""
        queue = bus.subscribe("meeting-two")
        try:
            await agent_routes.agent_respond(
                respond_command("meeting-two", "agent-a", "corr-a")
            )
            await agent_routes.agent_respond(
                respond_command("meeting-two", "agent-b", "corr-b")
            )
            events = await drain_until_idle(queue, idle_count=2)
        finally:
            bus.unsubscribe("meeting-two", queue)

        for event in events:
            if event["type"] == "audit.event":
                continue
            expected = (
                "corr-a" if event["agentInstanceId"] == "agent-a" else "corr-b"
            )
            assert event["correlationId"] == expected

    async def test_meeting_scoping_no_leak(self):
        """Subscriber on another meetingId never sees the events."""
        scoped = bus.subscribe("meeting-scoped")
        other = bus.subscribe("meeting-other")
        try:
            await agent_routes.agent_respond(
                respond_command("meeting-scoped", "agent-a", "corr-s")
            )
            await drain_until_idle(scoped)
            assert other.qsize() == 0
        finally:
            bus.unsubscribe("meeting-scoped", scoped)
            bus.unsubscribe("meeting-other", other)

    async def test_reconnect_does_not_replay(self):
        """After a completed sequence, a fresh subscriber gets nothing."""
        queue = bus.subscribe("meeting-replay")
        try:
            await agent_routes.agent_respond(
                respond_command("meeting-replay", "agent-a", "corr-r")
            )
            await drain_until_idle(queue)
        finally:
            bus.unsubscribe("meeting-replay", queue)

        fresh = bus.subscribe("meeting-replay")
        try:
            with pytest.raises(TimeoutError):
                async with asyncio.timeout(0.3):
                    await fresh.get()
        finally:
            bus.unsubscribe("meeting-replay", fresh)


class TestOwnerScoping:
    """Ticket #5: meetingId is claimed by the first tenant that touches it."""

    def test_respond_wrong_tenant_rejected(self, client):
        """Second respond for the same meetingId from a different tenant → 403."""
        first = respond_command("meeting-scope-1", "agent-a", "corr-1")
        first["scope"]["tenantId"] = "tenant-owner"
        ok = client.post("/agent/respond", json=first)
        assert ok.status_code == 202

        second = respond_command("meeting-scope-1", "agent-a", "corr-2")
        second["scope"]["tenantId"] = "tenant-intruder"
        denied = client.post("/agent/respond", json=second)
        assert denied.status_code == 403
        assert denied.json()["detail"] == "tenant_mismatch"

    def test_respond_same_tenant_repeat_ok(self, client):
        """Repeat commands from the SAME tenant for a claimed meeting stay 202."""
        cmd1 = respond_command("meeting-scope-2", "agent-a", "corr-1")
        cmd1["scope"]["tenantId"] = "tenant-owner"
        assert client.post("/agent/respond", json=cmd1).status_code == 202

        cmd2 = respond_command("meeting-scope-2", "agent-b", "corr-2")
        cmd2["scope"]["tenantId"] = "tenant-owner"
        assert client.post("/agent/respond", json=cmd2).status_code == 202

    def test_events_missing_header_rejected(self, client):
        response = client.get("/agent/events/meeting-scope-3")
        assert response.status_code == 403
        assert response.json()["detail"] == "missing_tenant_header"

    async def test_events_wrong_tenant_rejected(self):
        cmd = respond_command("meeting-scope-4", "agent-a", "corr-1")
        cmd["scope"]["tenantId"] = "tenant-owner"
        await agent_routes.agent_respond(cmd)

        with pytest.raises(HTTPException) as exc_info:
            await agent_routes.agent_events_stream(
                "meeting-scope-4", x_tenant_id="tenant-intruder"
            )
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "tenant_mismatch"

    async def test_events_correct_tenant_allowed(self):
        cmd = respond_command("meeting-scope-5", "agent-a", "corr-1")
        cmd["scope"]["tenantId"] = "tenant-owner"
        await agent_routes.agent_respond(cmd)

        response = await agent_routes.agent_events_stream(
            "meeting-scope-5", x_tenant_id="tenant-owner"
        )
        assert response.media_type == "text/event-stream"

    async def test_events_unclaimed_meeting_allowed_any_tenant(self):
        """A meeting nobody has responded to yet has nothing to leak — any
        tenant may open the stream (it will just see no events)."""
        response = await agent_routes.agent_events_stream(
            "meeting-scope-unclaimed", x_tenant_id="tenant-anyone"
        )
        assert response.media_type == "text/event-stream"

    async def test_denial_emits_audit_event(self):
        """A rejected respond call still publishes a scope/denied audit.event
        onto the (rightful owner's) meeting bus."""
        queue = bus.subscribe("meeting-scope-6")
        try:
            first = respond_command("meeting-scope-6", "agent-a", "corr-1")
            first["scope"]["tenantId"] = "tenant-owner"
            assert (await agent_routes.agent_respond(first))["correlationId"] == "corr-1"

            second = respond_command("meeting-scope-6", "agent-a", "corr-2")
            second["scope"]["tenantId"] = "tenant-intruder"
            with pytest.raises(HTTPException) as exc_info:
                await agent_routes.agent_respond(second)
            assert exc_info.value.status_code == 403

            events = []
            while not queue.empty():
                events.append(queue.get_nowait().model_dump())
            denials = [
                e
                for e in events
                if e["type"] == "audit.event" and e["payload"]["action"] == "scope/denied"
            ]
            assert len(denials) == 1
            assert denials[0]["payload"]["actor"] == "tenant/tenant-intruder"
        finally:
            bus.unsubscribe("meeting-scope-6", queue)


class TestSSEGenerator:
    """The SSE endpoint's generator: retry directive, data frames, heartbeat."""

    async def test_stream_emits_data_and_heartbeat(self, monkeypatch):
        monkeypatch.setattr(agent_routes, "HEARTBEAT_SECONDS", 0.2)
        response = await agent_routes.agent_events_stream(
            "meeting-sse", x_tenant_id="tenant-sse"
        )
        assert response.media_type == "text/event-stream"
        stream = response.body_iterator

        first = await anext(stream)
        assert first.startswith("retry:")

        event = AgentStatusEvent(
            type="agent.status",
            meetingId="meeting-sse",
            agentInstanceId="agent-a",
            ts="2026-07-02T00:00:00+00:00",
            correlationId="corr-sse",
            payload=AgentStatusPayload(status="thinking"),
        )
        await bus.publish("meeting-sse", event)

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
        await bus.publish("meeting-sse", event)
