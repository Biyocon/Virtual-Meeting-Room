---
id: "#7"
title: "Tabletop-integration: AgentCard ind i rigtigt meeting-UI"
milestone: "M2+ (før M6)"
status: draft
prioritet: "P1"
deps:
  - "M2-gate"
blocks:
  - "M6-UI"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

`app/page.tsx` er stadig den statiske v0-mockup (hardcodede deltagere, fake "Duration: 45:23", døde knapper). Det fungerende AgentCard lever kun på `/agent-demo`. PRD P0 kræver tabletop-layout med 4+ agent-kort, MeetingControls med AlertDialog og a11y. Bevidst udskudt fra M1 — men skal ligge FØR M6 (LiveKit-UI bygger ovenpå).

## Done ser sådan ud

Forsiden viser et digitalt bord med 4 live agent-kort (fra profiler, #6), speaking-states drevet af rigtige events, fungerende MeetingControls (forlad-bekræftelse), fuld tab-navigation.

## Teknisk scope

- [ ] `components/tabletop/` — bord-layout 6–8 pladser (1440px primary)
- [ ] Erstat mock-deltagere i `app/page.tsx` med AgentCard-instanser fra profiler
- [ ] MeetingControls: mic/kamera(stub)/forlad med AlertDialog + agent-panel-toggle
- [ ] AgentChatPanel (sidebar): delta-streaming + auto-scroll
- [ ] Status-debounce på hurtige state-skift (udestående M1-risikomitigering)
- [ ] A11y-audit: tab-navigation + ARIA på hele MeetingRoom

## Acceptkriterie

- [ ] 4 agent-kort rundt om bord på 1440px; alle med disclosure-badge
- [ ] Status-skift < 500ms fra event til DOM (PRD §6)
- [ ] Forlad-knap → AlertDialog; Tab når hele rummet
- [ ] Ingen ændringer i `useAgentEvents.ts`-kontrakten

## Blocker / noter

2026-07-01: Aktiveres når M2-gate er passeret. Overvej Playwright-test for latency-metrikken.
