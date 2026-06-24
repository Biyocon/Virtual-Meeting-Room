// The swap seam (ADR-0005 DoD): UI and BFF depend only on AgentRuntime.
// M0 binds it to the in-process TS stub. M2 binds it to the Python sidecar over
// HTTP/SSE — with no change to the UI, the contract, or the BFF routes.

import type { AgentCommand } from "./contract"

export interface AgentRuntime {
  // Accepts a validated command and drives the response by publishing
  // AgentEvents onto the bus. Returns once the command is accepted (202),
  // not once the (streamed) response is complete.
  respond(command: AgentCommand): Promise<void>
}

import { stubRuntime } from "./stub"

function httpSidecarRuntime(baseUrl: string): AgentRuntime {
  return {
    async respond(command: AgentCommand) {
      const res = await fetch(`${baseUrl}/agent/respond`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(command),
      })
      if (res.status !== 202) {
        throw new Error(
          `Sidecar respond failed: ${res.status} ${await res.text()}`
        )
      }
    },
  }
}

export function getAgentRuntime(): AgentRuntime {
  const sidecarUrl = process.env.NEXT_PUBLIC_AGENT_SIDECAR_URL
  return sidecarUrl
    ? httpSidecarRuntime(sidecarUrl)
    : stubRuntime
}
