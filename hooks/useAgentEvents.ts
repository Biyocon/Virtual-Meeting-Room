"use client"

// SSE client for the Agent Event Contract. Subscribes to one meeting's stream
// and reduces the events into render-ready state for AgentCard.
//
// No browser storage (guardrail): state lives in React only. EventSource handles
// reconnect natively (the server sends `retry:`); we de-dupe finals by
// correlationId so a reconnect mid-stream never double-applies.

import { useEffect, useRef, useState } from "react"
import type { AgentEvent, AgentStatus } from "@/lib/agent/contract"

export type AgentView = {
  status: AgentStatus
  streamingText: string
  finalText: string | null
  connected: boolean
}

const INITIAL: AgentView = { status: "idle", streamingText: "", finalText: null, connected: false }

export function useAgentEvents(meetingId: string, tenantId: string, agentInstanceId?: string): AgentView {
  const [view, setView] = useState<AgentView>(INITIAL)
  const seenFinals = useRef<Set<string>>(new Set())

  useEffect(() => {
    if (!meetingId || !tenantId) return
    // tenantId as a query param (#5): EventSource can't set custom headers,
    // so this is how the BFF learns which tenant is asking (see
    // app/api/agent/events/[meetingId]/route.ts).
    const source = new EventSource(
      `/api/agent/events/${encodeURIComponent(meetingId)}?tenantId=${encodeURIComponent(tenantId)}`,
    )

    source.addEventListener("ready", () => setView((v) => ({ ...v, connected: true })))

    source.onmessage = (msg) => {
      let event: AgentEvent
      try {
        event = JSON.parse(msg.data) as AgentEvent
      } catch {
        return
      }
      // Only react to events for this card's agent (when one is specified).
      if (agentInstanceId && event.agentInstanceId && event.agentInstanceId !== agentInstanceId) return

      switch (event.type) {
        case "agent.status":
          setView((v) => ({ ...v, status: event.payload.status }))
          break
        case "agent.message.delta":
          setView((v) => ({ ...v, streamingText: v.streamingText + event.payload.text, finalText: null }))
          break
        case "agent.message.final": {
          if (seenFinals.current.has(event.correlationId)) break
          seenFinals.current.add(event.correlationId)
          setView((v) => ({ ...v, finalText: event.payload.text, streamingText: event.payload.text }))
          break
        }
        default:
          break
      }
    }

    source.onerror = () => setView((v) => ({ ...v, connected: false }))

    return () => source.close()
  }, [meetingId, tenantId, agentInstanceId])

  return view
}
