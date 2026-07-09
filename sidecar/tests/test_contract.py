"""Contract validation: Python models ↔ TS JSON schema."""

import json
from pathlib import Path

import pytest

from agent_sidecar.contracts import (
    AgentAddCommand,
    AgentRespondCommand,
    AgentStatusEvent,
    AgentMessageDeltaEvent,
    AgentMessageFinalEvent,
    AuditEventModel,
    OwnerScope,
    AgentProfile,
    MeetingAgentInstance,
)


def load_json_schema() -> dict:
    """Load TS JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "lib" / "agent" / "agent-event.schema.json"
    with open(schema_path) as f:
        return json.load(f)


class TestAgentCommandContract:
    """Validate AgentCommand types match JSON schema."""

    def test_agent_add_command_shape(self):
        """agent.add command matches schema."""
        cmd = AgentAddCommand(
            type="agent.add",
            scope=OwnerScope(tenantId="t1", meetingId="m1"),
            correlationId="corr-1",
            payload={"agentProfileId": "ap-1", "role": "analyst"},
        )
        assert cmd.type == "agent.add"
        assert cmd.scope.tenantId == "t1"
        assert "agent.add" in load_json_schema()["commandTypes"]

    def test_agent_respond_command_shape(self):
        """agent.respond command matches schema."""
        cmd = AgentRespondCommand(
            type="agent.respond",
            scope=OwnerScope(
                tenantId="t1", meetingId="m1", agentInstanceId="ai-1"
            ),
            correlationId="corr-1",
            payload={"agentInstanceId": "ai-1", "prompt": "Hello"},
        )
        assert cmd.type == "agent.respond"
        assert cmd.payload.prompt == "Hello"
        assert "agent.respond" in load_json_schema()["commandTypes"]


class TestAgentEventContract:
    """Validate AgentEvent types match JSON schema."""

    def test_agent_status_event_shape(self):
        """agent.status event matches schema."""
        event = AgentStatusEvent(
            type="agent.status",
            meetingId="m1",
            agentInstanceId="ai-1",
            ts="2026-06-24T10:00:00Z",
            correlationId="corr-1",
            payload={"status": "thinking"},
        )
        assert event.type == "agent.status"
        assert event.payload.status in ["idle", "listening", "thinking", "speaking"]
        assert "agent.status" in load_json_schema()["eventTypes"]

    def test_agent_message_delta_event_shape(self):
        """agent.message.delta event matches schema."""
        event = AgentMessageDeltaEvent(
            type="agent.message.delta",
            meetingId="m1",
            agentInstanceId="ai-1",
            ts="2026-06-24T10:00:00Z",
            correlationId="corr-1",
            payload={"text": "Hello"},
        )
        assert event.type == "agent.message.delta"
        assert event.payload.text == "Hello"
        assert "agent.message.delta" in load_json_schema()["eventTypes"]

    def test_agent_message_final_event_shape(self):
        """agent.message.final event matches schema."""
        event = AgentMessageFinalEvent(
            type="agent.message.final",
            meetingId="m1",
            agentInstanceId="ai-1",
            ts="2026-06-24T10:00:00Z",
            correlationId="corr-1",
            payload={"text": "Final message", "citations": None},
        )
        assert event.type == "agent.message.final"
        assert event.payload.text == "Final message"
        assert "agent.message.final" in load_json_schema()["eventTypes"]

    def test_audit_event_shape(self):
        """audit.event event matches schema."""
        event = AuditEventModel(
            type="audit.event",
            meetingId="m1",
            agentInstanceId="ai-1",
            ts="2026-06-24T10:00:00Z",
            correlationId="corr-1",
            payload={"actor": "agent/ai-1", "action": "command/agent.respond"},
        )
        assert event.type == "audit.event"
        assert event.payload.actor == "agent/ai-1"
        assert "audit.event" in load_json_schema()["eventTypes"]


class TestContractEnvelopeValidation:
    """Envelope fields are required per schema."""

    def test_event_requires_meeting_id(self):
        """meetingId is required."""
        with pytest.raises(ValueError):
            AgentStatusEvent(
                type="agent.status",
                meetingId="",  # Empty
                agentInstanceId="ai-1",
                ts="2026-06-24T10:00:00Z",
                correlationId="corr-1",
                payload={"status": "idle"},
            )

    def test_event_requires_correlation_id(self):
        """correlationId is required."""
        with pytest.raises(ValueError):
            AgentStatusEvent(
                type="agent.status",
                meetingId="m1",
                agentInstanceId="ai-1",
                ts="2026-06-24T10:00:00Z",
                correlationId="",  # Empty
                payload={"status": "idle"},
            )


class TestRuntimeEntities:
    """AgentProfile and MeetingAgentInstance shapes."""

    def test_agent_profile_requires_id_and_name(self):
        with pytest.raises(ValueError):
            AgentProfile(name="Test", role="role")

    def test_agent_profile_accepts_minimal_valid_data(self):
        profile = AgentProfile(id="p1", name="Test", role="role")
        assert profile.id == "p1"
        assert profile.accentColor == "#004E51"

    def test_meeting_agent_instance_requires_scope(self):
        with pytest.raises(ValueError):
            MeetingAgentInstance(agentInstanceId="ai-1", agentProfileId="p1", role="role")
