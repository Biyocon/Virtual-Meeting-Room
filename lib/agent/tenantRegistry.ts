// Owner-scoping (ticket #5) — BFF-side mirror of the sidecar's tenant
// registry (sidecar/src/agent_sidecar/main.py). Dev-only, in-memory,
// process-local (same seam as ./bus.ts) — a real registry lands when
// meetings persist beyond one process. Enforced on both sides: the BFF
// rejects before it ever forwards to the sidecar (defense in depth).
//
// globalThis-backed (not a plain module-level `const`): Next.js dev mode
// re-executes route modules on Fast Refresh/on-demand compilation, which
// would otherwise silently reset a plain module-level Map between the first
// requests to different routes — verified by hand (curl) during #5: a
// module-level Map showed `size: 0` from the events route immediately after
// the respond route had already registered a meeting into "its own" copy.
// Attaching to globalThis survives re-execution within the same process.
// Production builds don't hot-reload, so this is a no-op there.

declare global {
  // eslint-disable-next-line no-var
  var __agentTenantRegistry: Map<string, string> | undefined
}

const tenantRegistry = globalThis.__agentTenantRegistry ?? new Map<string, string>()
globalThis.__agentTenantRegistry = tenantRegistry

export class TenantMismatchError extends Error {
  constructor(
    public readonly meetingId: string,
    public readonly expected: string,
    public readonly actual: string,
  ) {
    super(`meeting ${meetingId} is owned by a different tenant`)
  }
}

// Used by POST /api/agent/respond: the first command for a meetingId claims
// it for that tenant; later commands from a different tenantId are rejected.
export function claimOrCheckTenant(meetingId: string, tenantId: string): void {
  const existing = tenantRegistry.get(meetingId)
  if (existing === undefined) {
    tenantRegistry.set(meetingId, tenantId)
    return
  }
  if (existing !== tenantId) {
    throw new TenantMismatchError(meetingId, existing, tenantId)
  }
}

// Used by GET /api/agent/events/[meetingId]: never claims ownership —
// subscribing must not be able to squat a meetingId before its owner's
// first command claims it. Unclaimed meetings have nothing to leak, so any
// tenant may open the stream; it will simply see no events.
export function checkTenantReadOnly(meetingId: string, tenantId: string): void {
  const existing = tenantRegistry.get(meetingId)
  if (existing !== undefined && existing !== tenantId) {
    throw new TenantMismatchError(meetingId, existing, tenantId)
  }
}

// Test-only: reset between test cases (mirrors the pytest autouse fixture).
export function __resetTenantRegistryForTests(): void {
  tenantRegistry.clear()
}
