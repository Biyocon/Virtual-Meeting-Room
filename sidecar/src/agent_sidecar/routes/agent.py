"""Agent sidecar HTTP routes.

Mirrors the BFF's agent endpoints behind the Agent Event Contract. No real
model/TTS/STT/RAG yet (M3+).
"""

import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import StreamingResponse

from agent_sidecar.audit import publish_audit_event, publish_scope_denied
from agent_sidecar.contracts import (
    AgentAddCommand,
    AgentCommand,
    AgentEvent,
    AgentMessageDeltaEvent,
    AgentMessageDeltaPayload,
    AgentMessageFinalEvent,
    AgentMessageFinalPayload,
    AgentRespondCommand,
    AgentStatusEvent,
    AgentStatusPayload,
    KnowledgeScopeSetCommand,
    ToolApproveCommand,
)
from agent_sidecar.runtime.instance import create_instance, get_instance, update_instance_status
from agent_sidecar.runtime.profile_loader import get_profiles
from agent_sidecar.runtime.state import (
    HEARTBEAT_SECONDS,
    DELTA_DELAY_SECONDS,
    TenantMismatch,
    bus,
    claim_or_check_tenant,
    check_tenant_readonly,
    now_iso,
)


router = APIRouter()

# Keep strong refs to in-flight respond sequences (create_task is weakly held).
_background_tasks: set[asyncio.Task] = set()


def _status_event(
    meeting_id: str,
    agent_instance_id: str,
    correlation_id: str,
    value: str,
) -> AgentStatusEvent:
    return AgentStatusEvent(
        type="agent.status",
        meetingId=meeting_id,
        agentInstanceId=agent_instance_id,
        ts=now_iso(),
        correlationId=correlation_id,
        payload=AgentStatusPayload(status=value),  # type: ignore[arg-type]
    )


async def run_respond_sequence(cmd: AgentRespondCommand) -> None:
    """Emit the synthetic respond sequence for ONE command.

    IDs come from the command — never generated here. Real inference replaces
    the canned deltas in M3+; the event choreography stays.
    """
    meeting_id = cmd.scope.meetingId
    agent_id = cmd.payload.agentInstanceId
    corr_id = cmd.correlationId

    # Mark instance as thinking.
    update_instance_status(meeting_id=meeting_id, tenant_id=cmd.scope.tenantId, agent_instance_id=agent_id, status="thinking")
    await bus.publish(meeting_id, _status_event(meeting_id, agent_id, corr_id, "thinking"))

    deltas = ["Hello", " from", " Python", " sidecar"]

    await asyncio.sleep(DELTA_DELAY_SECONDS)
    for text in deltas:
        await bus.publish(
            meeting_id,
            AgentMessageDeltaEvent(
                type="agent.message.delta",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=now_iso(),
                correlationId=corr_id,
                payload=AgentMessageDeltaPayload(text=text),
            ),
        )
        await asyncio.sleep(DELTA_DELAY_SECONDS)

    update_instance_status(meeting_id=meeting_id, tenant_id=cmd.scope.tenantId, agent_instance_id=agent_id, status="speaking")
    await bus.publish(meeting_id, _status_event(meeting_id, agent_id, corr_id, "speaking"))
    await bus.publish(
        meeting_id,
        AgentMessageFinalEvent(
            type="agent.message.final",
            meetingId=meeting_id,
            agentInstanceId=agent_id,
            ts=now_iso(),
            correlationId=corr_id,
            payload=AgentMessageFinalPayload(text="".join(deltas), citations=None),
        ),
    )

    update_instance_status(meeting_id=meeting_id, tenant_id=cmd.scope.tenantId, agent_instance_id=agent_id, status="idle")
    await bus.publish(meeting_id, _status_event(meeting_id, agent_id, corr_id, "idle"))


def _parse_command(cmd: dict) -> AgentCommand:
    """Parse a raw dict into the correct AgentCommand subtype."""
    cmd_type = cmd.get("type")
    if cmd_type == "agent.add":
        return AgentAddCommand(**cmd)
    if cmd_type == "agent.respond":
        return AgentRespondCommand(**cmd)
    if cmd_type == "knowledgeScope.set":
        return KnowledgeScopeSetCommand(**cmd)
    if cmd_type == "tool.approve":
        return ToolApproveCommand(**cmd)
    raise ValueError(f"Unknown command type: {cmd_type}")


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok", "service": "agent-sidecar", "version": "M2"}


@router.post("/agent/respond", status_code=status.HTTP_202_ACCEPTED)
async def agent_respond(cmd: dict) -> dict[str, str]:
    """TS BFF → Sidecar: trigger agent action.

    Validates command against AgentCommand contract. Returns 202 immediately;
    events stream to UI via /agent/events SSE.
    """
    try:
        parsed = _parse_command(cmd)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    correlation_id = parsed.correlationId
    scope = parsed.scope
    meeting_id = scope.meetingId
    tenant_id = scope.tenantId

    # Canonical agent instance id for this command:
    # - agent.respond: payload is authoritative (scope.agentInstanceId is optional)
    # - agent.add: derive from scope or profile id
    if isinstance(parsed, AgentRespondCommand):
        agent_id = parsed.payload.agentInstanceId
    elif isinstance(parsed, AgentAddCommand):
        agent_id = scope.agentInstanceId or f"{parsed.payload.agentProfileId}-{correlation_id[:8]}"
    else:
        agent_id = scope.agentInstanceId

    try:
        claim_or_check_tenant(meeting_id, tenant_id)
    except TenantMismatch as mismatch:
        await publish_scope_denied(mismatch.meeting_id, mismatch.expected, mismatch.actual)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="tenant_mismatch")

    # Emit audit.event for the command.
    await publish_audit_event(
        meeting_id=meeting_id,
        agent_instance_id=agent_id,
        correlation_id=correlation_id,
        actor=f"agent/{agent_id or 'unknown'}",
        action=f"command/{parsed.type}",
    )

    # agent.add creates/updates the runtime instance.
    if isinstance(parsed, AgentAddCommand):
        profiles = get_profiles()
        profile = profiles.get(parsed.payload.agentProfileId)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unknown_agent_profile:{parsed.payload.agentProfileId}",
            )
        create_instance(
            tenant_id=tenant_id,
            meeting_id=meeting_id,
            agent_instance_id=agent_id,
            profile=profile,
            role=parsed.payload.role,
        )
        await publish_audit_event(
            meeting_id=meeting_id,
            agent_instance_id=agent_id,
            correlation_id=correlation_id,
            actor=f"agent/{agent_id}",
            action="instance/created",
            target=f"profile/{parsed.payload.agentProfileId}",
        )

    # agent.respond drives the event stream (M2 DoD); other command types are
    # audited only until their runtimes exist (M3+).
    if isinstance(parsed, AgentRespondCommand):
        # Resolve instance (must exist or we cannot attribute events).
        try:
            get_instance(tenant_id=tenant_id, meeting_id=meeting_id, agent_instance_id=agent_id)
        except Exception:
            # Auto-create a stub instance from a default profile so the demo
            # keeps working when callers send respond without a preceding add.
            profiles = get_profiles()
            fallback_profile = next(iter(profiles.values()))
            create_instance(
                tenant_id=tenant_id,
                meeting_id=meeting_id,
                agent_instance_id=agent_id,
                profile=fallback_profile,
                role="fallback",
            )

        task = asyncio.create_task(run_respond_sequence(parsed))
        _background_tasks.add(task)
        task.add_done_callback(_background_tasks.discard)

    return {"correlationId": correlation_id}


@router.get("/agent/events/{meeting_id}")
async def agent_events_stream(
    meeting_id: str,
    x_tenant_id: str | None = Header(default=None, alias="x-tenant-id"),
) -> StreamingResponse:
    """UI/BFF → Sidecar: SSE stream of agent events (meeting-scoped).

    Subscribes to the meeting bus: events appear only when commands drive
    them (POST /agent/respond). Nothing is replayed on reconnect. Heartbeat
    comment every HEARTBEAT_SECONDS keeps proxies from closing the stream.

    Owner-scoped (#5): requires x-tenant-id. Rejected with 403 if missing,
    or if the meetingId is already claimed by a different tenant.
    """
    if not x_tenant_id:
        await publish_scope_denied(meeting_id, "required", "missing")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="missing_tenant_header"
        )

    try:
        check_tenant_readonly(meeting_id, x_tenant_id)
    except TenantMismatch as mismatch:
        await publish_scope_denied(
            mismatch.meeting_id, mismatch.expected, mismatch.actual
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="tenant_mismatch"
        )

    queue = bus.subscribe(meeting_id)

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            yield "retry: 3000\n\n"
            while True:
                try:
                    event: AgentEvent = await asyncio.wait_for(
                        queue.get(), timeout=HEARTBEAT_SECONDS
                    )
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
                    continue
                yield f"data: {event.model_dump_json()}\n\n"
        finally:
            bus.unsubscribe(meeting_id, queue)

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )
