---
id: "#5"
title: "Owner-scoping på events-endpoints"
milestone: "M2"
status: active
prioritet: "P1"
deps:
  - "#2"
blocks: []
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

Alle kan i dag GET'e enhver meetingId's event-stream — ingen tenant-check nogen steder. Testplanens scoping-test ("forkert tenantId afvises") er uimplementérbar fordi intet lag kender gyldige tenants. M2 bruger kun testdata (ADR-0003), men scoping-mekanikken skal PÅ PLADS før M5 (rigtige filer i RAG).

## Done ser sådan ud

Events- og respond-endpoints kræver tenant-kontekst; forkert/manglende tenantId → 403. MVP-mekanisme: delt header-token + tenantId-match (rigtig auth kommer i M8).

## Teknisk scope

- [ ] Definér MVP-scoping: `x-tenant-id` header valideres mod meeting-registrering (in-memory registry i sidecar)
- [ ] BFF videresender tenant-kontekst til sidecar; afviser selv ved mismatch
- [ ] Sidecar: 403 ved ukendt meetingId/tenantId-kombination
- [ ] `audit.event` ved afviste forsøg
- [ ] Tests: forkert tenant → 403 (pytest + TS-integrationstest)

## Relevante filer

- `app/api/agent/events/[meetingId]/route.ts`
- `app/api/agent/respond/route.ts`
- `sidecar/src/agent_sidecar/main.py`
- `lib/agent/contract.ts` (OwnerScope — tenantId/meetingId er allerede påkrævet i kontrakten)

## Acceptkriterie

- [ ] Korrekt tenant: fuld funktionalitet uændret
- [ ] Forkert tenantId → 403 + audit.event
- [ ] Manglende tenant-header → 403
- [ ] Scoping-test fra testplan §6 grøn i CI

## Blocker / noter

2026-07-01: Bevidst SIMPEL mekanisme — Entra ID kommer først i M8. Undgå at bygge auth-system her.
