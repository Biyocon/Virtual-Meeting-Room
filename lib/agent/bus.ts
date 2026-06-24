// ⚠️ DEV STUB ONLY — in-memory, single-process event bus.
//
// This is NOT a production design. It works only inside one `next dev` Node
// process: the /respond route publishes here, the /events SSE route subscribes.
// In production the SSE stream is served by the Python sidecar (ADR-0005) over a
// real transport (a broker / the sidecar's own SSE), and this file goes away.
//
// Guardrail: keep this seam thin so swapping it out never touches UI or contract.

import { EventEmitter } from "node:events"
import type { AgentEvent } from "./contract"

// Survive HMR in dev by stashing the emitter on globalThis (otherwise each
// module reload would create a fresh, disconnected bus).
const globalForBus = globalThis as unknown as { __agentBus?: EventEmitter }

const bus = globalForBus.__agentBus ?? new EventEmitter()
bus.setMaxListeners(0)
if (!globalForBus.__agentBus) globalForBus.__agentBus = bus

const channel = (meetingId: string) => `meeting:${meetingId}`

export function publish(event: AgentEvent): void {
  bus.emit(channel(event.meetingId), event)
}

export function subscribe(meetingId: string, listener: (event: AgentEvent) => void): () => void {
  bus.on(channel(meetingId), listener)
  return () => bus.off(channel(meetingId), listener)
}
