// TS stub runtime (M0/M1). Emits a realistic event sequence behind the Agent
// Event Contract so the UI can be built before the Python sidecar exists.
//
// ⚠️ No real model or TTS calls (those are M2/M3). Testdata only.
// On `agent.respond`: agent.status:thinking → 3–5 agent.message.delta →
//                     agent.message.final → agent.status:idle.

import type { AgentCommand, AgentEvent, AgentStatus } from "./contract"
import type { AgentRuntime } from "./sidecarClient"
import { publish } from "./bus"

const DELTA_TEXT = [
  "Lad mig se på projektdata for det her. ",
  "Ud fra den seneste mappe ser jeg tre punkter, ",
  "vi bør tage stilling til på mødet. ",
  "Jeg foreslår, at vi prioriterer kontrakt-kontrakten først, ",
  "og parkerer resten til næste iteration.",
]

const wait = (ms: number) => new Promise((r) => setTimeout(r, ms))

function statusEvent(command: AgentCommand, status: AgentStatus): AgentEvent {
  return {
    type: "agent.status",
    meetingId: command.scope.meetingId,
    agentInstanceId: command.scope.agentInstanceId,
    ts: new Date().toISOString(),
    correlationId: command.correlationId,
    payload: { status },
  }
}

async function runRespond(command: AgentCommand): Promise<void> {
  if (command.type !== "agent.respond") return
  const { meetingId, agentInstanceId } = command.scope

  publish(statusEvent(command, "thinking"))
  await wait(400)

  let full = ""
  for (const chunk of DELTA_TEXT) {
    full += chunk
    publish({
      type: "agent.message.delta",
      meetingId,
      agentInstanceId,
      ts: new Date().toISOString(),
      correlationId: command.correlationId,
      payload: { text: chunk },
    })
    await wait(250)
  }

  publish(statusEvent(command, "speaking"))
  publish({
    type: "agent.message.final",
    meetingId,
    agentInstanceId,
    ts: new Date().toISOString(),
    correlationId: command.correlationId,
    // KnowledgeScope is a stub in M0, but the citations slot is wired (M5 fills it).
    payload: { text: full, citations: [] },
  })

  await wait(1200)
  publish(statusEvent(command, "idle"))
}

export const stubRuntime: AgentRuntime = {
  async respond(command) {
    // Fire-and-forget the streamed sequence; resolve immediately (202 semantics).
    void runRespond(command)
  },
}
