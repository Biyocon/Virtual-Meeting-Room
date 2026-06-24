// Agent Event Contract — single source of truth (TS side).
// Mirrored language-neutrally in ./agent-event.schema.json for the future
// Python sidecar (ADR-0005). Keep the two in sync; scripts/agent-contract.test.mjs
// fails CI on drift.
//
// Principle (ADR-0005): Biyocon owns the product surface (body); the Python
// sidecar owns the intelligence (brain). Everything flows behind THIS contract,
// so the M0 TS stub can later be swapped for the real sidecar without UI change.

import { z } from "zod"

// ── Owner-scoping ────────────────────────────────────────────────────────────
// Every runtime entity carries tenantId + meetingId (+ agentInstanceId where it
// applies). Enforced on every call. (stage-2-architecture §3)
export const OwnerScope = z.object({
  tenantId: z.string().min(1),
  meetingId: z.string().min(1),
  agentInstanceId: z.string().min(1).optional(),
})
export type OwnerScope = z.infer<typeof OwnerScope>

// ── Agent status ─────────────────────────────────────────────────────────────
export const AGENT_STATUSES = ["idle", "listening", "thinking", "speaking"] as const
export const AgentStatus = z.enum(AGENT_STATUSES)
export type AgentStatus = z.infer<typeof AgentStatus>

// ── Shared event envelope ────────────────────────────────────────────────────
const Envelope = {
  meetingId: z.string().min(1),
  agentInstanceId: z.string().min(1).optional(),
  ts: z.string().min(1), // ISO-8601
  correlationId: z.string().min(1),
}

const KnowledgeRef = z.object({
  sourceId: z.string(),
  label: z.string().optional(),
  locator: z.string().optional(),
})
export type KnowledgeRef = z.infer<typeof KnowledgeRef>

// ── Server / sidecar → client events ─────────────────────────────────────────
export const AgentEvent = z.discriminatedUnion("type", [
  z.object({ ...Envelope, type: z.literal("agent.status"), payload: z.object({ status: AgentStatus }) }),
  z.object({ ...Envelope, type: z.literal("agent.message.delta"), payload: z.object({ text: z.string() }) }),
  z.object({
    ...Envelope,
    type: z.literal("agent.message.final"),
    payload: z.object({ text: z.string(), citations: z.array(KnowledgeRef).optional() }),
  }),
  z.object({
    ...Envelope,
    type: z.literal("agent.audio"),
    payload: z.object({ audioUrl: z.string().optional(), chunk: z.string().optional(), format: z.string() }),
  }),
  z.object({
    ...Envelope,
    type: z.literal("agent.action"),
    payload: z.object({ kind: z.enum(["decision", "action_item"]), data: z.unknown() }),
  }),
  z.object({
    ...Envelope,
    type: z.literal("agent.tool.approval_request"),
    payload: z.object({ toolId: z.string(), args: z.unknown(), reason: z.string() }),
  }),
  z.object({
    ...Envelope,
    type: z.literal("meeting.summary"),
    payload: z.object({
      summary: z.string(),
      decisions: z.array(z.string()),
      actionItems: z.array(z.string()),
    }),
  }),
  z.object({
    ...Envelope,
    type: z.literal("audit.event"),
    payload: z.object({ actor: z.string(), action: z.string(), target: z.string().optional() }),
  }),
])
export type AgentEvent = z.infer<typeof AgentEvent>
export type AgentEventType = AgentEvent["type"]

// ── Client → BFF → sidecar commands ──────────────────────────────────────────
export const AgentCommand = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("agent.add"),
    scope: OwnerScope,
    correlationId: z.string().min(1),
    payload: z.object({ agentProfileId: z.string(), role: z.string() }),
  }),
  z.object({
    type: z.literal("agent.respond"),
    scope: OwnerScope,
    correlationId: z.string().min(1),
    payload: z.object({
      agentInstanceId: z.string().min(1),
      prompt: z.string().optional(),
      knowledgeScopeId: z.string().optional(),
    }),
  }),
  z.object({
    type: z.literal("knowledgeScope.set"),
    scope: OwnerScope,
    correlationId: z.string().min(1),
    payload: z.object({ sources: z.array(z.object({ kind: z.string(), ref: z.string() })) }),
  }),
  z.object({
    type: z.literal("tool.approve"),
    scope: OwnerScope,
    correlationId: z.string().min(1),
    payload: z.object({ approvalId: z.string(), approved: z.boolean() }),
  }),
])
export type AgentCommand = z.infer<typeof AgentCommand>
export type AgentCommandType = AgentCommand["type"]

// ── Core runtime entities (subset needed for M0–M1) ──────────────────────────
// Full datamodel lives in docs/architecture/stage-2-architecture.md §3.
export const Meeting = z.object({
  meetingId: z.string(),
  tenantId: z.string(),
  ownerId: z.string(),
  sharedBrainId: z.string().optional(),
  dataClassification: z.literal("test_only"), // MVP constraint (ADR-0003)
  createdAt: z.string(),
})
export type Meeting = z.infer<typeof Meeting>

export const MeetingAgentInstance = z.object({
  agentInstanceId: z.string(),
  meetingId: z.string(),
  tenantId: z.string(),
  agentProfileId: z.string(),
  role: z.string(),
  status: AgentStatus,
  joinedAt: z.string(),
})
export type MeetingAgentInstance = z.infer<typeof MeetingAgentInstance>
