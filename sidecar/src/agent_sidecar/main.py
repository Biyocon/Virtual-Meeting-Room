"""Agent event contract sidecar: Python/FastAPI implementation (M2 stub).

Mirrors lib/agent/contract.ts (TS source of truth). Validates all inputs/outputs
against the contract. No real model/TTS/STT/RAG yet (M3+).
"""

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncGenerator, Literal, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ── Contract: OwnerScope ──────────────────────────────────────────────────


class OwnerScope(BaseModel):
    tenantId: str = Field(..., min_length=1)
    meetingId: str = Field(..., min_length=1)
    agentInstanceId: str | None = Field(None, min_length=1)


# ── Contract: AgentCommand (mirror lib/agent/contract.ts) ──────────────────

class AgentAddPayload(BaseModel):
    agentProfileId: str
    role: str


class AgentRespondPayload(BaseModel):
    agentInstanceId: str = Field(..., min_length=1)
    prompt: str | None = None
    knowledgeScopeId: str | None = None


class KnowledgeScopeSetPayload(BaseModel):
    sources: list[dict] = Field(default_factory=list)


class ToolApprovePayload(BaseModel):
    approvalId: str
    approved: bool


class AgentAddCommand(BaseModel):
    type: Literal["agent.add"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: AgentAddPayload


class AgentRespondCommand(BaseModel):
    type: Literal["agent.respond"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: AgentRespondPayload


class KnowledgeScopeSetCommand(BaseModel):
    type: Literal["knowledgeScope.set"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: KnowledgeScopeSetPayload


class ToolApproveCommand(BaseModel):
    type: Literal["tool.approve"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: ToolApprovePayload


# ── Contract: AgentEvent (mirror lib/agent/contract.ts) ────────────────────

class AgentStatusPayload(BaseModel):
    status: Literal["idle", "listening", "thinking", "speaking"]


class AgentMessageDeltaPayload(BaseModel):
    text: str


class KnowledgeRef(BaseModel):
    sourceId: str
    label: str | None = None
    locator: str | None = None


class AgentMessageFinalPayload(BaseModel):
    text: str
    citations: list[KnowledgeRef] | None = None


class AgentAudioPayload(BaseModel):
    audioUrl: str | None = None
    chunk: str | None = None
    format: str


class AgentActionPayload(BaseModel):
    kind: Literal["decision", "action_item"]
    data: dict


class ToolApprovalRequestPayload(BaseModel):
    toolId: str
    args: dict
    reason: str


class MeetingSummaryPayload(BaseModel):
    summary: str
    decisions: list[str]
    actionItems: list[str]


class AuditEventPayload(BaseModel):
    actor: str
    action: str
    target: str | None = None


# Envelope (common to all events)
class AgentEventBase(BaseModel):
    meetingId: str = Field(..., min_length=1)
    agentInstanceId: str | None = Field(None, min_length=1)
    ts: str = Field(...)  # ISO-8601
    correlationId: str = Field(..., min_length=1)

    class Config:
        extra = "forbid"


class AgentStatusEvent(AgentEventBase):
    type: Literal["agent.status"]
    payload: AgentStatusPayload


class AgentMessageDeltaEvent(AgentEventBase):
    type: Literal["agent.message.delta"]
    payload: AgentMessageDeltaPayload


class AgentMessageFinalEvent(AgentEventBase):
    type: Literal["agent.message.final"]
    payload: AgentMessageFinalPayload


class AgentAudioEvent(AgentEventBase):
    type: Literal["agent.audio"]
    payload: AgentAudioPayload


class AgentActionEvent(AgentEventBase):
    type: Literal["agent.action"]
    payload: AgentActionPayload


class ToolApprovalRequestEvent(AgentEventBase):
    type: Literal["agent.tool.approval_request"]
    payload: ToolApprovalRequestPayload


class MeetingSummaryEvent(AgentEventBase):
    type: Literal["meeting.summary"]
    payload: MeetingSummaryPayload


class AuditEventModel(AgentEventBase):
    type: Literal["audit.event"]
    payload: AuditEventPayload


# Union of all valid events
AgentEvent = Union[
    AgentStatusEvent,
    AgentMessageDeltaEvent,
    AgentMessageFinalEvent,
    AgentAudioEvent,
    AgentActionEvent,
    ToolApprovalRequestEvent,
    MeetingSummaryEvent,
    AuditEventModel,
]


# ── Lifespan ──────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown logic."""
    print("[sidecar] Booting agent sidecar (Python/FastAPI M2 stub)")
    # TODO M3+: Initialize model, TTS/STT, runtime
    yield
    print("[sidecar] Shutdown")


# ── FastAPI app ───────────────────────────────────────────────────────────


app = FastAPI(title="Agent Sidecar", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok", "service": "agent-sidecar", "version": "M2"}


@app.post("/agent/respond", status_code=status.HTTP_202_ACCEPTED)
async def agent_respond(cmd: dict) -> dict[str, str]:
    """
    TS BFF → Sidecar: trigger agent action.

    Validates command against AgentCommand contract. Returns 202 immediately;
    events stream to UI via /agent/events SSE.
    """
    try:
        # Parse and validate union type (discriminated by 'type' field)
        if cmd.get("type") == "agent.add":
            parsed = AgentAddCommand(**cmd)
        elif cmd.get("type") == "agent.respond":
            parsed = AgentRespondCommand(**cmd)
        elif cmd.get("type") == "knowledgeScope.set":
            parsed = KnowledgeScopeSetCommand(**cmd)
        elif cmd.get("type") == "tool.approve":
            parsed = ToolApproveCommand(**cmd)
        else:
            raise ValueError(f"Unknown command type: {cmd.get('type')}")

        correlation_id = parsed.correlationId
        scope = parsed.scope

        # Emit audit.event
        audit_event = AuditEventModel(
            type="audit.event",
            meetingId=scope.meetingId,
            agentInstanceId=scope.agentInstanceId,
            ts=datetime.now(timezone.utc).isoformat(),
            correlationId=correlation_id,
            payload=AuditEventPayload(
                actor=f"agent/{scope.agentInstanceId or 'unknown'}",
                action=f"command/{parsed.type}",
                target=None,
            ),
        )
        print(
            f"[sidecar] audit.event: correlationId={correlation_id} "
            f"action={parsed.type} meetingId={scope.meetingId}"
        )

        # TODO M3+: enqueue command, trigger model inference, stream events
        return {"correlationId": correlation_id}

    except Exception as e:
        print(f"[sidecar] Error in /agent/respond: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@app.get("/agent/events/{meeting_id}")
async def agent_events_stream(meeting_id: str) -> StreamingResponse:
    """
    UI → Sidecar: SSE stream of agent events (meeting-scoped).

    Stub implementation: emits synthetic sequence matching lib/agent/stub.ts
    for M0→M2 verification. Real events (M3+) come from model/TTS/RAG.
    """

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for the meeting (stub sequence)."""
        agent_id = "agent-0"
        corr_id = str(uuid4())

        # Stub sequence (mirrors lib/agent/stub.ts for testing)
        events: list[AgentEvent] = [
            AgentStatusEvent(
                type="agent.status",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentStatusPayload(status="thinking"),
            ),
            AgentMessageDeltaEvent(
                type="agent.message.delta",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentMessageDeltaPayload(text="Hello"),
            ),
            AgentMessageDeltaEvent(
                type="agent.message.delta",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentMessageDeltaPayload(text=" from"),
            ),
            AgentMessageDeltaEvent(
                type="agent.message.delta",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentMessageDeltaPayload(text=" Python"),
            ),
            AgentMessageDeltaEvent(
                type="agent.message.delta",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentMessageDeltaPayload(text=" sidecar"),
            ),
            AgentStatusEvent(
                type="agent.status",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentStatusPayload(status="speaking"),
            ),
            AgentMessageFinalEvent(
                type="agent.message.final",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentMessageFinalPayload(
                    text="Hello from Python sidecar",
                    citations=None,
                ),
            ),
            AgentStatusEvent(
                type="agent.status",
                meetingId=meeting_id,
                agentInstanceId=agent_id,
                ts=datetime.now(timezone.utc).isoformat(),
                correlationId=corr_id,
                payload=AgentStatusPayload(status="idle"),
            ),
        ]

        for event in events:
            data = event.model_dump_json()
            yield f"data: {data}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
