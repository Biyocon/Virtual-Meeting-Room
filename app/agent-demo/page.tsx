"use client"

// M0–M1 demo route — standalone on purpose. It mounts exactly ONE AgentCard
// behind the Agent Event Contract and does NOT touch the existing meeting
// mockup (app/page.tsx). Wiring the card into the real tabletop is a later
// milestone; keeping this isolated is the "no broad tabletop refactor" guardrail.
//
// Testdata only. The "respond" button hits the BFF, which drives the TS stub.

import { Button } from "@/components/ui/button"
import { AgentCard } from "@/components/agent-card"
import { useAgentEvents } from "@/hooks/useAgentEvents"
import type { AgentCommand } from "@/lib/agent/contract"

// Owner-scoped testdata (tenantId / meetingId / agentInstanceId).
const SCOPE = {
  tenantId: "tenant-test",
  meetingId: "meeting-demo-001",
  agentInstanceId: "agent-abdi-asis-pm",
}

export default function AgentDemoPage() {
  const view = useAgentEvents(SCOPE.meetingId, SCOPE.tenantId, SCOPE.agentInstanceId)

  async function handleRespond() {
    const command: AgentCommand = {
      type: "agent.respond",
      scope: SCOPE,
      correlationId: crypto.randomUUID(),
      payload: { agentInstanceId: SCOPE.agentInstanceId, prompt: "Hvad bør vi prioritere?" },
    }
    await fetch("/api/agent/respond", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(command),
    })
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 to-purple-700 p-8 flex flex-col items-center gap-6">
      <div className="text-center text-white">
        <h1 className="text-xl font-bold">Agent Event Contract — M0/M1 demo</h1>
        <p className="text-sm opacity-80">
          Ét agent-kort drevet af stub-runtime via SSE.{" "}
          <span className={view.connected ? "text-emerald-300" : "text-amber-300"}>
            {view.connected ? "● forbundet" : "○ ikke forbundet"}
          </span>
        </p>
      </div>

      <AgentCard
        name="Abdi Asis"
        role="Technical Product Manager"
        agentLabel="Stub v0"
        colorAccent="violet"
        status={view.status}
        text={view.finalText ?? view.streamingText}
      />

      <Button onClick={handleRespond} className="bg-purple-600 hover:bg-purple-700">
        Lad agenten svare
      </Button>
    </main>
  )
}
