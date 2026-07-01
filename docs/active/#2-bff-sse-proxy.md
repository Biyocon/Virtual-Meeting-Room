---
id: "#2"
title: "BFF SSE-proxy af sidecar-stream"
milestone: "M2"
status: active
prioritet: "P0"
deps:
  - "#1"
blocks:
  - "#3"
  - "#5"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

BFF'ens events-endpoint lytter kun på den lokale in-memory bus. Når `AGENT_SIDECAR_URL` er sat, går respond-kommandoer til Python — men UI'et ser aldrig sidecarens events. Nuværende default-tilstand (`.env.local` peger på sidecar) er derfor brudt end-to-end. Kommentaren i routen lover allerede: "From M2 this proxies the Python sidecar's stream instead".

## Done ser sådan ud

Med sidecar-URL sat modtager `/agent-demo` alle events fra Python-sidecaren gennem det UÆNDREDE BFF-endpoint `GET /api/agent/events/[meetingId]`. Uden URL: uændret stub-adfærd. Ingen ændringer i `hooks/useAgentEvents.ts` eller komponenter (det ER DoD'en).

## Teknisk scope

- [ ] `app/api/agent/events/[meetingId]/route.ts`: hvis sidecar-URL sat → fetch sidecar-SSE og pipe events igennem; ellers → lokal bus (nuværende adfærd)
- [ ] Abort-propagation: klient lukker → sidecar-fetch afbrydes
- [ ] Fejlhåndtering: sidecar nede → SSE-fejl-event + `retry`, ikke hængende request
- [ ] BFF'ens egne `audit.event`s merges fortsat ind i streamen
- [ ] Guard `controller.enqueue` efter close (kendt race i nuværende route)

## Relevante filer

- `app/api/agent/events/[meetingId]/route.ts`
- `lib/agent/sidecarClient.ts:34` (URL-læsning — omdøbes til `AGENT_SIDECAR_URL` i #8, koordinér)
- `lib/agent/bus.ts`

## Acceptkriterie

- [ ] `/agent-demo` viser fuld sekvens drevet af sidecar, nul ændringer i hooks/komponenter
- [ ] Stub-mode fungerer uændret uden env-var
- [ ] Sidecar-nedetid giver synlig fejl inden 5s, ingen hængende forbindelse
- [ ] Klient-disconnect lukker upstream-forbindelsen (verificér i sidecar-log)

## Blocker / noter

2026-07-01: Blokeret af #1 (sidecar skal have noget ægte at streame først).
