# Primer

Rewrite this file completely at the end of every session. Read it first at the
start of every session. If it goes stale it lies, and a lying primer is worse than none.

Read at session start: 1. `primer.md` → 2. `tasks/lessons.md` (durable rules).

---

## Project

- **Name:** Virtual Meeting Room (VMR) — AI-agenter med syntetisk stemme som ligestillede mødedeltagere
- **Root:** `C:\Users\Biyocon\virtual-meeting-room`
- **Stack:** Next.js 15 + React 19 + TS (BFF/UI) · Python FastAPI (sidecar) · pnpm · Zod/Pydantic-kontrakt
- **Git:** branch `feature/python-sidecar-m2`; main = PR-mål
- **Planning docs:** `docs/PRD.md` (v1.2), `docs/KØREPLAN.md`, `docs/DEPS.md`, tickets i `docs/active/`

---

## Current Focus (2026-07-09)

- **M2: Sidecar v0** — DoD: TS-stub → Python-sidecar-swap UDEN UI-ændring
- #1 ✅ · #2 ✅ · #3 ✅ · #4 ✅ · #5 ✅ · #6 ✅ · **M2-gate ✅ GODKENDT** — klar til M3 ∥ M4

## Verified This Session (2026-07-09)

- **QA-gate: AFVIST → GODKENDT:** Claude fandt under uafhængig QA en kritisk stil-crash når `scope.agentInstanceId` var udeladt men `payload.agentInstanceId` sat. Buggen var kontrakt-lovlig men ikke dækket af pytest, fordi testdata altid satte felterne ens. Fix: `routes/agent.py` bruger nu `payload.agentInstanceId` konsekvent. Ny regressionstest tilføjet (`test_agent_respond_payload_instance_id_without_scope`). Re-verificeret: 41/41 pytest, contract-test OK, tsc OK, manuel curl-E2E OK. Fuld rapport: `docs/qa/release-2026-07-09.md`.
- **#5 owner-scoping implementeret og E2E-verificeret**: sidecar-tenant-registry + BFF-mirror (`lib/agent/tenantRegistry.ts`); `/agent/events` kræver `x-tenant-id`; mismatch/manglende → 403 + `audit.event`. Regression bekræftet intakt efter #6. Detaljer: `docs/plans/m2-sidecar-v0.md` §"#5 Owner-scoping — implementeringsnote".
- **#6 struktur-split + AgentProfile-loader implementeret og testet**: `main.py` split til `contracts.py`, `routes/agent.py`, `runtime/state.py`, `runtime/profile_loader.py`, `runtime/instance.py`, `audit.py`; 3 YAML-profiler (`pm`, `analyst`, `facilitator`); `MeetingAgentInstance`-livscyklus; Pydantic v2 `ConfigDict(extra="forbid")` overalt; `sys.path.insert` fjernet fra tests. 41/41 pytest grønne efter fix. Detaljer: `docs/plans/m2-sidecar-v0.md` §"#6 Struktur-split + AgentProfile-loader — implementeringsnote".
- **Dev-mode-fund:** almindelige modul-niveau singletons (`const x = new Map()`) nulstilles af Next.js hot-reload på tværs af routes — verificeret under #5. Rettet i `tenantRegistry.ts` med `globalThis`-backed singleton. `bus.ts` bruger samme mønster og er IKKE rettet.
- Tidligere (2026-07-02): alle 3 DoD-brud for #1–#4 lukket og E2E-verificeret; `git diff hooks/ components/` var tom for DEN ændring (uændret krav — #5 rørte med vilje `hooks/useAgentEvents.ts` + `app/agent-demo/page.tsx` for at sende tenantId med, hvilket er forventet scope for #5, ikke et DoD-brud på #1-4's regel).
- mirotalksfu-adapter-sporet (eksploreret tidligere i dag) parkeret — modstred ADR-0001/0003/0005. Se `docs/_parked/`.

## Status Overview

| Item | Status | Summary |
|------|--------|---------|
| M0 kontrakt | ✅ | Zod + schema + drift-test + BFF-ruter |
| M1 agent-kort | ✅ | Kun `/agent-demo`; tabletop = draft #7 |
| M2 sidecar | ✅ | #1–#6 + qa-gate godkendt |
| CI | ✅ (ikke rekørt denne session — se Notes) | Contract+tsc+build+pytest grønne lokalt |
| M3–M9 | ⬜ | Se KØREPLAN; alt blokeret af M2 |

## Important Files

- `docs/plans/m2-sidecar-v0.md` — teknisk design for M2 — nu inkl. #5- og #6-noter
- `lib/agent/contract.ts` + `sidecar/src/agent_sidecar/contracts.py` — kontraktens to sider
- `sidecar/src/agent_sidecar/routes/agent.py` — endpoints
- `sidecar/src/agent_sidecar/runtime/` — state, profile_loader, instance
- `sidecar/profiles/*.yaml` — agent personaer
- `lib/agent/sidecarClient.ts` — swap-seamet
- `lib/agent/tenantRegistry.ts` (#5) — BFF-side owner-scoping, globalThis-singleton

## Blockers

- Ingen tekniske. Åbne beslutninger (ikke-blokerende nu): LiveKit Scale-tier (2026-08-15), LICENSE (før distribution), GDPR-review (2026-09-01)

## Next Steps

1. Commit M2-arbejdet (#5, #6, qa-gate) på `feature/python-sidecar-m2`
2. Kør CI (GitHub Actions)
3. Merge til main → start M3 ∥ M4

## Notes

- Commit-beskeden "M2: Complete sidecar implementation" (`f3f4a77`) overdriver — stol på tickets, ikke commit-historik
- `.env.local` har sidecar-URL sat → sidecar-mode virker nu NÅR uvicorn kører på :8000; uden sidecar: fjern env-var for stub-mode
- Testnote: httpx ASGITransport buffer'er hele responsen — uendelige SSE-streams kan ikke integrationstestes den vej; brug komponent-tests eller rigtig server
- #5 og #6 er IKKE committet endnu denne session (kun lokale filændringer + lokal verifikation) — commit på anmodning, jf. global CLAUDE.md
