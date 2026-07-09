"""Audit helpers: emit audit.event and scope-denied events on the meeting bus."""

from agent_sidecar.contracts import AuditEventModel, AuditEventPayload
from agent_sidecar.runtime.state import bus, now_iso


async def publish_audit_event(
    meeting_id: str,
    agent_instance_id: str | None,
    correlation_id: str,
    actor: str,
    action: str,
    target: str | None = None,
) -> None:
    """Publish an audit.event on the meeting bus."""
    await bus.publish(
        meeting_id,
        AuditEventModel(
            type="audit.event",
            meetingId=meeting_id,
            agentInstanceId=agent_instance_id,
            ts=now_iso(),
            correlationId=correlation_id,
            payload=AuditEventPayload(actor=actor, action=action, target=target),
        ),
    )


async def publish_scope_denied(
    meeting_id: str,
    expected: str,
    actual: str,
) -> None:
    """Publish an audit.event when tenant scoping rejects access."""
    await bus.publish(
        meeting_id,
        AuditEventModel(
            type="audit.event",
            meetingId=meeting_id,
            agentInstanceId=None,
            ts=now_iso(),
            correlationId=f"scope-denied-{meeting_id}-{actual}",
            payload=AuditEventPayload(
                actor=f"tenant/{actual}",
                action="scope/denied",
                target=f"meeting/{meeting_id} (owned by tenant/{expected})",
            ),
        ),
    )
