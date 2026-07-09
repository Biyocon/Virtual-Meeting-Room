"""MeetingAgentInstance lifecycle + in-memory registry.

Created by agent.add, updated by agent.respond, closed at meeting end. Every
instance carries owner-scope (tenantId + meetingId + agentInstanceId).
"""

from agent_sidecar.contracts import AgentProfile, AgentStatus, MeetingAgentInstance
from agent_sidecar.runtime.state import bus, now_iso


# Registry keyed by (tenantId, meetingId, agentInstanceId).
_instances: dict[tuple[str, str, str], MeetingAgentInstance] = {}


class InstanceNotFound(Exception):
    def __init__(self, tenant_id: str, meeting_id: str, agent_instance_id: str) -> None:
        super().__init__(
            f"agent instance not found: {agent_instance_id} in meeting {meeting_id} "
            f"for tenant {tenant_id}"
        )
        self.tenant_id = tenant_id
        self.meeting_id = meeting_id
        self.agent_instance_id = agent_instance_id


def create_instance(
    tenant_id: str,
    meeting_id: str,
    agent_instance_id: str,
    profile: AgentProfile,
    role: str,
) -> MeetingAgentInstance:
    """Create and register a new agent instance for a meeting."""
    key = (tenant_id, meeting_id, agent_instance_id)

    instance = MeetingAgentInstance(
        agentInstanceId=agent_instance_id,
        meetingId=meeting_id,
        tenantId=tenant_id,
        agentProfileId=profile.id,
        role=role,
        status="idle",
        joinedAt=now_iso(),
    )

    _instances[key] = instance
    return instance


def get_instance(
    tenant_id: str,
    meeting_id: str,
    agent_instance_id: str,
) -> MeetingAgentInstance:
    """Resolve an existing agent instance by owner-scope."""
    key = (tenant_id, meeting_id, agent_instance_id)
    instance = _instances.get(key)
    if instance is None:
        raise InstanceNotFound(tenant_id, meeting_id, agent_instance_id)
    return instance


def update_instance_status(
    tenant_id: str,
    meeting_id: str,
    agent_instance_id: str,
    status: AgentStatus,
) -> MeetingAgentInstance:
    """Update an instance's status and return the updated instance."""
    instance = get_instance(tenant_id, meeting_id, agent_instance_id)
    updated = instance.model_copy(update={"status": status})
    _instances[(tenant_id, meeting_id, agent_instance_id)] = updated
    return updated


def close_instance(
    tenant_id: str,
    meeting_id: str,
    agent_instance_id: str,
) -> MeetingAgentInstance | None:
    """Remove an instance from the registry and return it if it existed."""
    key = (tenant_id, meeting_id, agent_instance_id)
    return _instances.pop(key, None)


def list_instances_for_meeting(
    tenant_id: str,
    meeting_id: str,
) -> list[MeetingAgentInstance]:
    """List all active agent instances in a meeting."""
    return [
        instance
        for (t, m, _), instance in _instances.items()
        if t == tenant_id and m == meeting_id
    ]


def reset_instances() -> None:
    """Test-only: clear the registry between test cases."""
    _instances.clear()
