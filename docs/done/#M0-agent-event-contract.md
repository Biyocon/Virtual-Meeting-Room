---
id: "#M0"
title: "M0: Agent Event Contract + skeleton"
milestone: "M0"
status: done
afsluttet: "commit 93d60f1 (PR #4)"
oprettet: "2026-06-21"
sidst_opdateret: "2026-07-01"
---

## Leveret

- `lib/agent/contract.ts` — Zod discriminated unions: 8 event-typer + 4 command-typer, `OwnerScope` (tenantId/meetingId påkrævet), `Meeting`, `MeetingAgentInstance`, `dataClassification: "test_only"` (ADR-0003)
- `lib/agent/agent-event.schema.json` — sprogneutralt kontrakt-spejl
- `scripts/agent-contract.test.mjs` (`pnpm test:contract`) — drift-guard TS ↔ schema
- BFF: `app/api/agent/respond` (validering, 422, audit, 202) + `app/api/agent/events/[meetingId]` (SSE, heartbeat 15s, abort-cleanup)
- `lib/agent/bus.ts` (dev-only in-memory bus), `lib/agent/audit.ts` (stub), `lib/agent/sidecarClient.ts` (AgentRuntime-swap-seam)

## Kendte afvigelser (accepteret)

- Pydantic-kontrakt inline i `sidecar/main.py` i stedet for `contracts.py` → rettes i #6
- Drift-guard sammenligner kun typenavne, ikke payload-felter → udvides i #6

## Verifikation

`agent.status` flød UI ← BFF ← stub via SSE (manuel demo). Contract-test grøn.
