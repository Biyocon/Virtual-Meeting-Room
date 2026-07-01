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

## Current Focus (2026-07-01)

- **M2: Sidecar v0** — DoD: TS-stub → Python-sidecar-swap UDEN UI-ændring
- Første skridt: tickets **#1** (sidecar respond→events-kobling) og **#4** (CI) — kan køre parallelt

## Verified This Session

- M0 ✅ + M1 ✅ (isoleret demo på `/agent-demo`) — commit `93d60f1`, PR #4
- M2 er ~40%: scaffold + Pydantic-spejl + tests findes, men 3 DoD-brud bekræftet ved kode-audit:
  1. sidecar respond/events ukoblede (canned SSE-replay)
  2. BFF proxy'er ikke sidecar-stream (kun lokal bus)
  3. hardcoded `agent-0` vs UI-filter på ægte instanceId
- Docs-system fuldt realigneret 2026-07-01 (CHANGELOG-entry) — KØREPLAN/DEPS matcher nu kode + stage-3-plan

## Status Overview

| Item | Status | Summary |
|------|--------|---------|
| M0 kontrakt | ✅ | Zod + schema + drift-test + BFF-ruter |
| M1 agent-kort | ✅ | Kun `/agent-demo`; tabletop = draft #7 |
| M2 sidecar | ⏳ | Tickets #1–#6 i `docs/active/` |
| CI | ⬜ | Findes ikke (#4 — start straks) |
| M3–M9 | ⬜ | Se KØREPLAN; alt blokeret af M2 |

## Important Files

- `docs/plans/m2-sidecar-v0.md` — teknisk design for M2 (læs FØR implementering)
- `lib/agent/contract.ts` + `sidecar/src/agent_sidecar/main.py` — kontraktens to sider
- `lib/agent/sidecarClient.ts` — swap-seamet

## Blockers

- Ingen tekniske. Åbne beslutninger (ikke-blokerende nu): LiveKit Scale-tier (2026-08-15), LICENSE (før distribution), GDPR-review (2026-09-01)

## Next Steps

1. Implementér #1 (sidecar-bus, pytest-drevet) — design i `docs/plans/m2-sidecar-v0.md`
2. Parallelt: #4 (GitHub Actions: test:contract + tsc + pytest)
3. Derefter #2 → #3 → #5; #6 til sidst (efter #1 merget)
4. M2-gate: qa-release-tjek → M3 ∥ M4

## Notes

- Commit-beskeden "M2: Complete sidecar implementation" på denne branch overdriver — stol på tickets, ikke commit-historik
- `.env.local` har sidecar-URL sat → demo er p.t. brudt i sidecar-mode; stub-mode virker (fjern env-var)
