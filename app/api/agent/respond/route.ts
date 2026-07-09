// BFF command endpoint: client → BFF → (stub) runtime.
// Validates the AgentCommand against the contract, audits it, hands it to the
// runtime (stub in M0, Python sidecar from M2), and returns 202.

import { NextResponse } from "next/server"
import { AgentCommand } from "@/lib/agent/contract"
import { getAgentRuntime } from "@/lib/agent/sidecarClient"
import { emitAudit } from "@/lib/agent/audit"
import { claimOrCheckTenant, TenantMismatchError } from "@/lib/agent/tenantRegistry"

// Guardrail: Node.js runtime (not Edge) — the in-memory bus + SSE need a single
// long-lived Node process.
export const runtime = "nodejs"

export async function POST(req: Request) {
  let body: unknown
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: "invalid_json" }, { status: 400 })
  }

  const parsed = AgentCommand.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: "contract_violation", issues: parsed.error.issues }, { status: 422 })
  }
  const command = parsed.data

  // Owner-scoping (#5): the contract requires tenantId + meetingId to be
  // present; this claims/checks that meetingId actually belongs to that
  // tenantId (mirrors sidecar/src/agent_sidecar/main.py _claim_or_check_tenant).
  try {
    claimOrCheckTenant(command.scope.meetingId, command.scope.tenantId)
  } catch (err) {
    if (err instanceof TenantMismatchError) {
      return NextResponse.json({ error: "tenant_mismatch" }, { status: 403 })
    }
    throw err
  }

  emitAudit(command.scope, command.scope.agentInstanceId ?? "system", command.type, command.correlationId)

  await getAgentRuntime().respond(command)

  return NextResponse.json({ accepted: true, correlationId: command.correlationId }, { status: 202 })
}
