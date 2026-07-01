---
id: "#1"
title: "Sidecar-intern event-kobling: /agent/respond driver SSE-stream"
milestone: "M2"
status: active
prioritet: "P0"
deps: []
blocks:
  - "#2"
  - "#3"
  - "#6"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

I dag ignorerer sidecaren indkomne kommandoer: `POST /agent/respond` validerer og smider væk, mens `GET /agent/events/{meetingId}` afspiller en fast, kommando-uafhængig sekvens én gang per connect. M2-DoD ("swap uden UI-ændring") kræver at et respond-kald DRIVER event-streamen — ellers er sidecaren ikke en runtime, kun en attrap.

## Done ser sådan ud

Kald `POST /agent/respond` med en `agent.respond.request`-kommando → den åbne SSE-forbindelse for samme `meetingId` streamer thinking → delta(s) → speaking → final → idle, med kommandoens `correlationId` og `agentInstanceId`.

## Teknisk scope

- [ ] Meeting-scoped in-memory event-bus i sidecar (asyncio.Queue per meetingId, spejler `lib/agent/bus.ts`-mønstret)
- [ ] `/agent/respond` publicerer kommando til bus i stedet for at discarde
- [ ] Event-generator: kommando → synthetic svar-sekvens (LLM kommer i M3+) med ægte IDs fra kommandoen
- [ ] SSE-endpoint subscriber på bus i stedet for canned replay; heartbeat hvert 15s (spejl af BFF)
- [ ] Ingen replay af finals ved reconnect (correlationId genbruges IKKE per connection)
- [ ] pytest: respond → events-kobling, heartbeat, ingen duplikat-final ved reconnect

## Relevante filer

- `sidecar/src/agent_sidecar/main.py:1-366` (hele filen — split udskydes til #6)
- `lib/agent/bus.ts` (referencemønster)
- `sidecar/tests/test_endpoints.py`
- `docs/plans/m2-sidecar-v0.md` (design)

## Acceptkriterie

- [ ] POST respond → events synlige på allerede-åben SSE-stream inden 2s
- [ ] Events bærer kommandoens `correlationId` + `agentInstanceId` (ingen `agent-0`)
- [ ] Reconnect midt i sekvens giver ikke duplikat-final
- [ ] SSE-stream forbliver åben (heartbeat) — lukker ikke efter én sekvens
- [ ] Alle pytest grønne

## Blocker / noter

2026-07-01: Oprettet fra docs-drift-audit. Design i `docs/plans/m2-sidecar-v0.md`.
