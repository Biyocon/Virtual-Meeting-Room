// BFF event stream: server → client over SSE.
//
// Stub mode (no sidecar URL): subscribes to the in-process dev bus.
// Sidecar mode (M2): proxies the Python sidecar's SSE stream frame-by-frame
// through this same endpoint — same path, same wire format, no UI change.
// BFF-generated events (audit from the respond route) are merged in both modes.

import { NextResponse } from "next/server"
import { subscribe } from "@/lib/agent/bus"
import { getSidecarBaseUrl } from "@/lib/agent/sidecarClient"
import { checkTenantReadOnly, TenantMismatchError } from "@/lib/agent/tenantRegistry"

// Guardrail: Node.js runtime (not Edge) for a long-lived SSE connection.
export const runtime = "nodejs"
export const dynamic = "force-dynamic"

// Forward complete SSE frames only — re-framing here means locally generated
// frames can never be interleaved into the middle of a partial upstream frame.
async function proxySidecarStream(
  baseUrl: string,
  meetingId: string,
  tenantId: string,
  send: (data: string) => void,
  signal: AbortSignal,
) {
  const res = await fetch(
    `${baseUrl}/agent/events/${encodeURIComponent(meetingId)}`,
    {
      signal,
      headers: { Accept: "text/event-stream", "x-tenant-id": tenantId },
      cache: "no-store",
    },
  )
  if (!res.ok || !res.body) {
    throw new Error(`Sidecar events stream failed: ${res.status}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let frameEnd: number
    while ((frameEnd = buffer.indexOf("\n\n")) !== -1) {
      const frame = buffer.slice(0, frameEnd)
      buffer = buffer.slice(frameEnd + 2)
      if (frame.trim().length > 0) send(`${frame}\n\n`)
    }
  }
}

export async function GET(req: Request, { params }: { params: Promise<{ meetingId: string }> }) {
  const { meetingId } = await params
  const encoder = new TextEncoder()
  const sidecarUrl = getSidecarBaseUrl()

  // Owner-scoping (#5): EventSource can't set custom headers, so the client
  // passes tenantId as a query param; the BFF validates it itself (defense
  // in depth) before ever forwarding, then re-sends it as x-tenant-id to the
  // sidecar (mirrors sidecar/src/agent_sidecar/main.py agent_events_stream).
  const tenantId = new URL(req.url).searchParams.get("tenantId")
  if (!tenantId) {
    return NextResponse.json({ error: "missing_tenant_id" }, { status: 403 })
  }
  try {
    checkTenantReadOnly(meetingId, tenantId)
  } catch (err) {
    if (err instanceof TenantMismatchError) {
      return NextResponse.json({ error: "tenant_mismatch" }, { status: 403 })
    }
    throw err
  }

  const stream = new ReadableStream({
    start(controller) {
      let closed = false
      const send = (data: string) => {
        if (closed) return
        try {
          controller.enqueue(encoder.encode(data))
        } catch {
          closed = true
        }
      }

      // Open the stream and tell the client the retry/backoff window.
      send("retry: 3000\n\n")
      send(`event: ready\ndata: ${JSON.stringify({ meetingId })}\n\n`)

      // BFF's own events (audit from the respond route) in both modes.
      const unsubscribe = subscribe(meetingId, (event) => {
        send(`data: ${JSON.stringify(event)}\n\n`)
      })

      // Heartbeat keeps proxies from closing an idle connection.
      const heartbeat = setInterval(() => send(": ping\n\n"), 15000)

      const close = () => {
        if (closed) return
        closed = true
        clearInterval(heartbeat)
        unsubscribe()
        try {
          controller.close()
        } catch {
          /* already closed */
        }
      }

      if (sidecarUrl) {
        proxySidecarStream(sidecarUrl, meetingId, tenantId, send, req.signal).catch(
          (err: unknown) => {
            // Sidecar unreachable or stream broke: fail fast and visibly —
            // the client's EventSource reconnects per the retry directive.
            if (!req.signal.aborted) {
              // Named "sidecar-error" — a server event named "error" would
              // collide with EventSource's native error handling client-side.
              send(
                `event: sidecar-error\ndata: ${JSON.stringify({
                  message: err instanceof Error ? err.message : "sidecar stream error",
                })}\n\n`,
              )
            }
            close()
          },
        )
      }

      req.signal?.addEventListener?.("abort", close)
    },
  })

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  })
}
