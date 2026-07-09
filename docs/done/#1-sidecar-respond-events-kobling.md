---
id: "#1"
title: "Sidecar-intern event-kobling: /agent/respond driver SSE-stream"
milestone: "M2"
status: done
afsluttet: "2026-07-02"
prioritet: "P0"
deps: []
blocks:
  - "#2"
  - "#3"
  - "#6"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-02"
---

## Hvad & Hvorfor

I dag ignorerer sidecaren indkomne kommandoer: `POST /agent/respond` validerer og smider væk, mens `GET /agent/events/{meetingId}` afspiller en fast, kommando-uafhængig sekvens én gang per connect. M2-DoD ("swap uden UI-ændring") kræver at et respond-kald DRIVER event-streamen — ellers er sidecaren ikke en runtime, kun en attrap.

## Done ser sådan ud

Kald `POST /agent/respond` med en `agent.respond.request`-kommando → den åbne SSE-forbindelse for samme `meetingId` streamer thinking → delta(s) → speaking → final → idle, med kommandoens `correlationId` og `agentInstanceId`.

## Teknisk scope

- [x] Meeting-scoped in-memory event-bus i sidecar (asyncio.Queue per meetingId, spejler `lib/agent/bus.ts`-mønstret)
- [x] `/agent/respond` publicerer kommando til bus i stedet for at discarde
- [x] Event-generator: kommando → synthetic svar-sekvens (LLM kommer i M3+) med ægte IDs fra kommandoen
- [x] SSE-endpoint subscriber på bus i stedet for canned replay; heartbeat hvert 15s (spejl af BFF)
- [x] Ingen replay af finals ved reconnect (correlationId genbruges IKKE per connection)
- [x] pytest: respond → events-kobling, heartbeat, ingen duplikat-final ved reconnect

## Relevante filer

- `sidecar/src/agent_sidecar/main.py:1-366` (hele filen — split udskydes til #6)
- `lib/agent/bus.ts` (referencemønster)
- `sidecar/tests/test_endpoints.py`
- `docs/plans/m2-sidecar-v0.md` (design)

## Acceptkriterie

- [x] POST respond → events synlige på allerede-åben SSE-stream inden 2s
- [x] Events bærer kommandoens `correlationId` + `agentInstanceId` (ingen `agent-0`)
- [x] Reconnect midt i sekvens giver ikke duplikat-final
- [x] SSE-stream forbliver åben (heartbeat) — lukker ikke efter én sekvens
- [x] Alle pytest grønne (19/19)

## Blocker / noter

2026-07-01: Oprettet fra docs-drift-audit. Design i `docs/plans/m2-sidecar-v0.md`.

2026-07-02: DONE. MeetingBus + create_task-sekvens i main.py; 6 nye async tests (komponent-niveau — httpx ASGITransport kan ikke streame uendelig SSE; HTTP-E2E kommer i #2). IDs tages fra kommandoen — sidecar-siden af #3 dermed også løst.
