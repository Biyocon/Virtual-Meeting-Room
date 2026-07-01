---
id: "#3"
title: "Ægte agentInstanceId/correlationId end-to-end"
milestone: "M2"
status: done
afsluttet: "2026-07-02"
prioritet: "P0"
deps:
  - "#1"
  - "#2"
blocks: []
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-02"
---

## Hvad & Hvorfor

Sidecaren hardcoder `agent_id = "agent-0"`, mens demo-kortet filtrerer på `agent-abdi-asis-pm` — selv en fungerende proxy ville blive filtreret væk i `useAgentEvents`. IDs skal flyde fra kommando → sidecar → events → UI-filter.

## Done ser sådan ud

Det agent-kort der sendte kommandoen, og KUN det kort, reagerer på svaret. To kort i samme meeting med forskellige instanceIds blander ikke events.

## Teknisk scope

- [x] Sidecar: `agentInstanceId` + `correlationId` tages fra indkommende kommando, aldrig genereres til svar-events
- [x] BFF respond-route: verificér at command-payload allerede bærer IDs (contract.ts) — ingen omskrivning
- [x] Test: to samtidige kommandoer med forskellige instanceIds → korrekt adskilte event-sekvenser

## Relevante filer

- `sidecar/src/agent_sidecar/main.py` (event-generator fra #1)
- `hooks/useAgentEvents.ts` (filterlogik — må IKKE ændres)
- `app/agent-demo/page.tsx` (demo-scope: `tenant-test`/`meeting-demo-001`/`agent-abdi-asis-pm`)

## Acceptkriterie

- [x] Ingen forekomst af hardcoded `agent-0` i sidecar
- [x] Demo-kort reagerer på egne kommandoer via sidecar-path
- [x] pytest: 2 instanceIds → ingen krydskontaminering
- [x] `useAgentEvents.ts` uændret (diff tom)

## Blocker / noter

2026-07-01: Oprettet. Sidste DoD-brud af de tre fra audit-rapporten.

2026-07-02: DONE. Sidecar-siden løst i #1 (IDs fra kommandoen); E2E verificeret via #2-manuel test: events på BFF-endpointet bærer `agent-abdi-asis-pm` + kommandoens correlationId — præcis hvad useAgentEvents filtrerer på. `grep agent-0` = 0 hits. Visuel browser-bekræftelse indgår i M2-gatens qa-release-tjek.
