// Audit stub. Every agent action emits an AuditEvent (stage-2 §3, ADR-0005).
// M0: logs to the server console and publishes an `audit.event` onto the bus.
// Later: persisted to the App DB with retention/owner-scoping.

import type { AgentEvent, OwnerScope } from "./contract"
import { publish } from "./bus"

export function emitAudit(
  scope: OwnerScope,
  actor: string,
  action: string,
  correlationId: string,
  target?: string,
): void {
  const event: AgentEvent = {
    type: "audit.event",
    meetingId: scope.meetingId,
    agentInstanceId: scope.agentInstanceId,
    ts: new Date().toISOString(),
    correlationId,
    payload: { actor, action, target },
  }
  // Structured server-side log (testdata only in MVP).
  console.log("[audit]", JSON.stringify({ tenantId: scope.tenantId, ...event.payload, meetingId: scope.meetingId }))
  publish(event)
}
