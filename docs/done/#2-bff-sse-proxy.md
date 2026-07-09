---
id: "#2"
title: "BFF SSE-proxy af sidecar-stream"
milestone: "M2"
status: done
afsluttet: "2026-07-02"
prioritet: "P0"
deps:
  - "#1"
blocks:
  - "#3"
  - "#5"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-02"
---

## Hvad & Hvorfor

BFF'ens events-endpoint lytter kun på den lokale in-memory bus. Når `AGENT_SIDECAR_URL` er sat, går respond-kommandoer til Python — men UI'et ser aldrig sidecarens events. Nuværende default-tilstand (`.env.local` peger på sidecar) er derfor brudt end-to-end. Kommentaren i routen lover allerede: "From M2 this proxies the Python sidecar's stream instead".

## Done ser sådan ud

Med sidecar-URL sat modtager `/agent-demo` alle events fra Python-sidecaren gennem det UÆNDREDE BFF-endpoint `GET /api/agent/events/[meetingId]`. Uden URL: uændret stub-adfærd. Ingen ændringer i `hooks/useAgentEvents.ts` eller komponenter (det ER DoD'en).

## Teknisk scope

- [x] `app/api/agent/events/[meetingId]/route.ts`: hvis sidecar-URL sat → fetch sidecar-SSE og pipe events igennem; ellers → lokal bus (nuværende adfærd)
- [x] Abort-propagation: klient lukker → sidecar-fetch afbrydes
- [x] Fejlhåndtering: sidecar nede → SSE-fejl-event + `retry`, ikke hængende request
- [x] BFF'ens egne `audit.event`s merges fortsat ind i streamen
- [x] Guard `controller.enqueue` efter close (kendt race i nuværende route)

## Relevante filer

- `app/api/agent/events/[meetingId]/route.ts`
- `lib/agent/sidecarClient.ts:34` (URL-læsning — omdøbes til `AGENT_SIDECAR_URL` i #8, koordinér)
- `lib/agent/bus.ts`

## Acceptkriterie

- [x] `/agent-demo` viser fuld sekvens drevet af sidecar, nul ændringer i hooks/komponenter
- [x] Stub-mode fungerer uændret uden env-var
- [x] Sidecar-nedetid giver synlig fejl inden 5s, ingen hængende forbindelse
- [ ] Klient-disconnect lukker upstream-forbindelsen (verificér i sidecar-log)

## Blocker / noter

2026-07-01: Blokeret af #1 (sidecar skal have noget ægte at streame først).

2026-07-02: DONE. Betinget frame-atomisk proxy (re-framing på 

-grænser så lokale frames aldrig lander midt i en delvis upstream-frame). `getSidecarBaseUrl()` udskilt — `AGENT_SIDECAR_URL` kanonisk, NEXT_PUBLIC_-fallback til #8. Fejl sendes som `sidecar-error` (navnet `error` kolliderer med EventSource native).
Verificeret manuelt: (1) sidecar-mode fuld sekvens via BFF med ægte IDs, (2) stub-mode uændret, (3) sidecar nede → sidecar-error + lukning straks. Klient-disconnect: signal propageres til upstream-fetch (kode-verificeret, ikke log-verificeret).
