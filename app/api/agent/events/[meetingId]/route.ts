// BFF event stream: server → client over SSE. Subscribes to the (dev) bus for
// one meeting and forwards every AgentEvent. From M2 this proxies the Python
// sidecar's stream instead — same path, same wire format, no UI change.

import { subscribe } from "@/lib/agent/bus"

// Guardrail: Node.js runtime (not Edge) for a long-lived SSE connection.
export const runtime = "nodejs"
export const dynamic = "force-dynamic"

export async function GET(req: Request, { params }: { params: Promise<{ meetingId: string }> }) {
  const { meetingId } = await params
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    start(controller) {
      const send = (data: string) => controller.enqueue(encoder.encode(data))

      // Open the stream and tell the client the retry/backoff window.
      send("retry: 3000\n\n")
      send(`event: ready\ndata: ${JSON.stringify({ meetingId })}\n\n`)

      const unsubscribe = subscribe(meetingId, (event) => {
        send(`data: ${JSON.stringify(event)}\n\n`)
      })

      // Heartbeat keeps proxies from closing an idle connection.
      const heartbeat = setInterval(() => send(": ping\n\n"), 15000)

      req.signal?.addEventListener?.("abort", () => {
        clearInterval(heartbeat)
        unsubscribe()
        try {
          controller.close()
        } catch {
          /* already closed */
        }
      })
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
