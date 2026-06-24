"""Agent event contract sidecar: Python/FastAPI implementation."""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# — Contract mirrors (sync'd with lib/agent/contract.ts)


class AgentEntity(BaseModel):
    agentId: str
    tenantId: str
    meetingId: str
    agentInstanceId: str


class AuditEvent(BaseModel):
    auditId: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agentId: str
    tenantId: str
    meetingId: str
    action: str
    metadata: dict = Field(default_factory=dict)


class AgentCommand(BaseModel):
    """Posted by TS BFF to trigger agent action."""

    command: str
    agentInstanceId: str
    tenantId: str
    meetingId: str
    payload: dict = Field(default_factory=dict)


class AgentEvent(BaseModel):
    """Events streamed back to UI via SSE."""

    type: str  # thinking, delta, speaking, final, idle
    agentInstanceId: str
    tenantId: str
    meetingId: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    content: str | None = None
    metadata: dict = Field(default_factory=dict)


# — Lifespan


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown logic."""
    print("[sidecar] Booting agent sidecar (Python/FastAPI stub)")
    # TODO M2: Initialize model, TTS/STT, runtime
    yield
    print("[sidecar] Shutdown")


# — FastAPI app


app = FastAPI(title="Agent Sidecar", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok", "service": "agent-sidecar"}


@app.post("/agent/respond")
async def agent_respond(cmd: AgentCommand) -> dict[str, int]:
    """
    TS BFF → Sidecar: trigger agent action.
    Returns immediately with 202; events stream to UI via /agent/events SSE.
    """
    audit = AuditEvent(
        agentId="agent-0",  # TODO M2: resolve from cmd.agentInstanceId
        tenantId=cmd.tenantId,
        meetingId=cmd.meetingId,
        action=cmd.command,
        metadata=cmd.payload,
    )
    print(f"[sidecar] audit event: {audit.auditId} action={audit.action}")
    # TODO M2: enqueue command, trigger model/TTS
    return {"status": 202, "auditId": audit.auditId}


@app.get("/agent/events/{meeting_id}")
async def agent_events_stream(meeting_id: str) -> StreamingResponse:
    """
    UI → Sidecar: SSE stream of agent events.
    Stub: thinking → 5× delta → final → idle.
    """

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for the meeting."""
        # Stub flow: mirrors lib/agent/stub.ts for M0 verification
        events = [
            AgentEvent(
                type="thinking", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id
            ),
            AgentEvent(
                type="delta", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id, content="Hello"
            ),
            AgentEvent(
                type="delta", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id, content=" from"
            ),
            AgentEvent(
                type="delta", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id, content=" the"
            ),
            AgentEvent(
                type="delta", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id, content=" Python"
            ),
            AgentEvent(
                type="delta", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id, content=" sidecar"
            ),
            AgentEvent(
                type="speaking", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id
            ),
            AgentEvent(
                type="final", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id,
                content="Hello from the Python sidecar",
                metadata={"messageId": str(uuid4())},
            ),
            AgentEvent(
                type="idle", agentInstanceId="agent-0", tenantId="tenant-0",
                meetingId=meeting_id
            ),
        ]

        for event in events:
            data = event.model_dump_json()
            yield f"data: {data}\n\n"
            await asyncio.sleep(0.5)  # Simulate processing

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, host="127.0.0.1", port=8000,
        log_level="info"
    )
