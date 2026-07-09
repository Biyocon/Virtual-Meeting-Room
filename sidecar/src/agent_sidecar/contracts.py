"""Agent Event Contract — Python/Pydantic mirror of lib/agent/contract.ts.

Single source of truth for all wire shapes exchanged between BFF and sidecar.
Pydantic v2-style: model_config = ConfigDict(extra="forbid") everywhere.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ── Owner-scoping ────────────────────────────────────────────────────────────


class OwnerScope(BaseModel):
    tenantId: str = Field(..., min_length=1)
    meetingId: str = Field(..., min_length=1)
    agentInstanceId: str | None = Field(None, min_length=1)

    model_config = ConfigDict(extra="forbid")


# ── Agent status ─────────────────────────────────────────────────────────────

AgentStatus = Literal["idle", "listening", "thinking", "speaking"]


# ── AgentCommand payloads ────────────────────────────────────────────────────


class AgentAddPayload(BaseModel):
    agentProfileId: str
    role: str

    model_config = ConfigDict(extra="forbid")


class AgentRespondPayload(BaseModel):
    agentInstanceId: str = Field(..., min_length=1)
    prompt: str | None = None
    knowledgeScopeId: str | None = None

    model_config = ConfigDict(extra="forbid")


class KnowledgeScopeSetPayload(BaseModel):
    sources: list[dict] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class ToolApprovePayload(BaseModel):
    approvalId: str
    approved: bool

    model_config = ConfigDict(extra="forbid")


# ── AgentCommand discriminated union ─────────────────────────────────────────


class AgentAddCommand(BaseModel):
    type: Literal["agent.add"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: AgentAddPayload

    model_config = ConfigDict(extra="forbid")


class AgentRespondCommand(BaseModel):
    type: Literal["agent.respond"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: AgentRespondPayload

    model_config = ConfigDict(extra="forbid")


class KnowledgeScopeSetCommand(BaseModel):
    type: Literal["knowledgeScope.set"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: KnowledgeScopeSetPayload

    model_config = ConfigDict(extra="forbid")


class ToolApproveCommand(BaseModel):
    type: Literal["tool.approve"]
    scope: OwnerScope
    correlationId: str = Field(..., min_length=1)
    payload: ToolApprovePayload

    model_config = ConfigDict(extra="forbid")


# Convenience union used by route handlers.
AgentCommand = AgentAddCommand | AgentRespondCommand | KnowledgeScopeSetCommand | ToolApproveCommand


# ── AgentEvent payloads ──────────────────────────────────────────────────────


class AgentStatusPayload(BaseModel):
    status: AgentStatus

    model_config = ConfigDict(extra="forbid")


class AgentMessageDeltaPayload(BaseModel):
    text: str

    model_config = ConfigDict(extra="forbid")


class KnowledgeRef(BaseModel):
    sourceId: str
    label: str | None = None
    locator: str | None = None

    model_config = ConfigDict(extra="forbid")


class AgentMessageFinalPayload(BaseModel):
    text: str
    citations: list[KnowledgeRef] | None = None

    model_config = ConfigDict(extra="forbid")


class AgentAudioPayload(BaseModel):
    audioUrl: str | None = None
    chunk: str | None = None
    format: str

    model_config = ConfigDict(extra="forbid")


class AgentActionPayload(BaseModel):
    kind: Literal["decision", "action_item"]
    data: dict

    model_config = ConfigDict(extra="forbid")


class ToolApprovalRequestPayload(BaseModel):
    toolId: str
    args: dict
    reason: str

    model_config = ConfigDict(extra="forbid")


class MeetingSummaryPayload(BaseModel):
    summary: str
    decisions: list[str]
    actionItems: list[str]

    model_config = ConfigDict(extra="forbid")


class AuditEventPayload(BaseModel):
    actor: str
    action: str
    target: str | None = None

    model_config = ConfigDict(extra="forbid")


# ── AgentEvent discriminated union ───────────────────────────────────────────


class AgentEventBase(BaseModel):
    meetingId: str = Field(..., min_length=1)
    agentInstanceId: str | None = Field(None, min_length=1)
    ts: str = Field(..., min_length=1)  # ISO-8601
    correlationId: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


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


AgentEvent = (
    AgentStatusEvent
    | AgentMessageDeltaEvent
    | AgentMessageFinalEvent
    | AgentAudioEvent
    | AgentActionEvent
    | ToolApprovalRequestEvent
    | MeetingSummaryEvent
    | AuditEventModel
)


# ── Runtime entities ─────────────────────────────────────────────────────────


class AgentProfile(BaseModel):
    """Static configuration for an agent persona.

    Loaded from sidecar/profiles/*.yaml at startup. Mirrors the custom-format
    frontmatter expected by the TS side (id/name/role/avatar/accent/skills/
    systemPrompt) and adds M2 voice/knowledge stubs.
    """

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    description: str = ""
    avatar: str = ""  # URL/path placeholder; visual avatar lands in M6/M9
    accentColor: str = "#004E51"
    voiceProfile: dict = Field(default_factory=dict)  # M3 stub
    knowledgeScope: dict = Field(default_factory=dict)  # M5 stub
    skills: list[str] = Field(default_factory=list)
    systemPrompt: str = ""
    model: str = "gpt-4o-mini"
    capabilities: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class MeetingAgentInstance(BaseModel):
    """A single agent participating in a specific meeting.

    Created by agent.add, updated by agent.respond, closed at meeting end.
    Carries owner-scope on every runtime entity (tenantId + meetingId +
    agentInstanceId) per stage-2-architecture §3.
    """

    agentInstanceId: str = Field(..., min_length=1)
    meetingId: str = Field(..., min_length=1)
    tenantId: str = Field(..., min_length=1)
    agentProfileId: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    status: AgentStatus = "idle"
    joinedAt: str = Field(..., min_length=1)  # ISO-8601

    model_config = ConfigDict(extra="forbid")
