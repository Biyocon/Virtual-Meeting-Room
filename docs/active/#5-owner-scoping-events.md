---
id: "#5"
title: "Owner-scoping på events-endpoints"
milestone: "M2"
status: done
prioritet: "P1"
deps:
  - "#2"
blocks: []
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-09"
---

## Hvad & Hvorfor

Alle kan i dag GET'e enhver meetingId's event-stream — ingen tenant-check nogen steder. Testplanens scoping-test ("forkert tenantId afvises") er uimplementérbar fordi intet lag kender gyldige tenants. M2 bruger kun testdata (ADR-0003), men scoping-mekanikken skal PÅ PLADS før M5 (rigtige filer i RAG).

## Done ser sådan ud

Events- og respond-endpoints kræver tenant-kontekst; forkert/manglende tenantId → 403. MVP-mekanisme: delt header-token + tenantId-match (rigtig auth kommer i M8).

## Teknisk scope

- [x] Definér MVP-scoping: `x-tenant-id` header valideres mod meeting-registrering (in-memory registry i sidecar)
- [x] BFF videresender tenant-kontekst til sidecar; afviser selv ved mismatch
- [x] Sidecar: 403 ved ukendt meetingId/tenantId-kombination
- [x] `audit.event` ved afviste forsøg
- [x] Tests: forkert tenant → 403 (pytest + TS-integrationstest)

## Relevante filer

- `app/api/agent/events/[meetingId]/route.ts`
- `app/api/agent/respond/route.ts`
- `lib/agent/tenantRegistry.ts` (ny — BFF-side spejl)
- `sidecar/src/agent_sidecar/runtime/state.py` (tenant registry)
- `sidecar/src/agent_sidecar/routes/agent.py`
- `lib/agent/contract.ts` (OwnerScope — tenantId/meetingId er allerede påkrævet i kontrakten)

## Acceptkriterie

- [x] Korrekt tenant: fuld funktionalitet uændret
- [x] Forkert tenantId → 403 + audit.event
- [x] Manglende tenant-header → 403
- [x] Scoping-test fra testplan §6 grøn i CI

## Verifikation

- `pytest` i `sidecar/`: **40 passed** (2026-07-09)
- Manuelt curl-E2E: korrekt/forkert/manglende tenant på begge endpoints, uklaimet meeting
- `npx tsc --noEmit`: OK

## Blocker / noter

2026-07-09: #5 implementeret, testet og bevaret gennem #6-struktursplittet. Bemærk: Next.js dev-mode hot-reload nulstiller modul-niveau singletons; BFF-registry bruger `globalThis`-backing for at overleve Fast Refresh.
