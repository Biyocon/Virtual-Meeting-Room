"""Test sidecar endpoints."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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


class TestAgentEvents:
    """GET /agent/events/{meeting_id}."""

    def test_agent_events_stream_returns_sse(self, client):
        """GET /agent/events/{meeting_id} returns SSE stream."""
        response = client.get("/agent/events/meeting-1")
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

    def test_agent_events_stream_contains_events(self, client):
        """GET /agent/events/{meeting_id} yields valid events."""
        response = client.get("/agent/events/meeting-1")
        assert response.status_code == 200

        # Parse SSE events
        events = []
        for line in response.iter_lines():
            if line.startswith("data: "):
                import json
                try:
                    event = json.loads(line[6:])  # Skip "data: "
                    events.append(event)
                except json.JSONDecodeError:
                    pass

        # Stub sequence: status:thinking, 5× delta, status:speaking, final, status:idle
        assert len(events) >= 8
        assert events[0]["type"] == "agent.status"
        assert events[0]["payload"]["status"] == "thinking"
        assert any(e["type"] == "agent.message.delta" for e in events)
        assert any(e["type"] == "agent.message.final" for e in events)
        assert events[-1]["type"] == "agent.status"
        assert events[-1]["payload"]["status"] == "idle"

    def test_agent_events_meeting_id_in_events(self, client):
        """GET /agent/events/{meeting_id} includes meeting_id in events."""
        meeting_id = "meeting-123"
        response = client.get(f"/agent/events/{meeting_id}", timeout=30)

        import json
        for line in response.iter_lines():
            if line.startswith("data: "):
                try:
                    event = json.loads(line[6:])
                    assert event["meetingId"] == meeting_id
                except json.JSONDecodeError:
                    pass
                break  # Just check first event
