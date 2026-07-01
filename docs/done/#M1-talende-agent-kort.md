---
id: "#M1"
title: "M1: Én talende agent-kort (isoleret demo)"
milestone: "M1"
status: done
afsluttet: "commit 93d60f1 (PR #4)"
oprettet: "2026-06-21"
sidst_opdateret: "2026-07-01"
---

## Leveret

- `components/agent-card.tsx` — 4 states (idle/listening/thinking/speaking, danske labels), speaker-ring, animeret waveform, streaming-cursor, altid-synligt "Syntetisk stemme"-badge uden disable-prop (ADR-0004)
- `hooks/useAgentEvents.ts` — EventSource-klient, event→`AgentView`-reducer, correlationId-dedup af finals (reconnect-guard), ingen browser-storage
- `app/agent-demo/page.tsx` — standalone demo (scope: `tenant-test`/`meeting-demo-001`/`agent-abdi-asis-pm`)
- `lib/agent/stub.ts` — thinking → 5 deltas → speaking → final → idle

## Scope-afgrænsning (bevidst)

- IKKE integreret i tabletop-UI (`app/page.tsx` = statisk v0-mockup) → draft #7
- Status-debounce ikke implementeret → del af #7
- `hooks/useMeetingRealtime` + `components/tabletop/` fra planen findes ikke i repo — planens "genbrug"-antagelse var forkert (se LESSON.md)

## Verifikation

Manuel demo på `/agent-demo`: alle 4 states + streamet tekst + disclosure synligt.
