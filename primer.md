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

## Current Focus (2026-07-02)

- **M2: Sidecar v0** — DoD: TS-stub → Python-sidecar-swap UDEN UI-ændring
- #1 ✅ · #2 ✅ · #3 ✅ · #4 ✅ (CI grøn, 51s) · tilbage: **#5 owner-scoping** + **#6 profile-loader/struktur-split** → M2-gate (qa-tjek)

## Verified This Session

- **Alle 3 DoD-brud lukket og E2E-verificeret manuelt**: sidecar + Next dev kørende → POST via BFF → fuld sekvens (thinking→4 deltas→speaking→final→idle) på BFF-SSE med kommandoens IDs; `git diff hooks/ components/` TOM (selve DoD'en)
- Stub-mode uændret uden env-var; sidecar nede → `sidecar-error`-event + lukning straks
- CI grøn på PR #5 (run 28552701603, 51s); 19/19 pytest; tsc ren
- `AGENT_SIDECAR_URL` nu kanonisk (server-only); NEXT_PUBLIC_-fallback fjernes i #8

## Status Overview

| Item | Status | Summary |
|------|--------|---------|
| M0 kontrakt | ✅ | Zod + schema + drift-test + BFF-ruter |
| M1 agent-kort | ✅ | Kun `/agent-demo`; tabletop = draft #7 |
| M2 sidecar | ⏳ | #1–#4 ✅; tilbage: #5, #6, qa-gate |
| CI | ✅ | Grøn på PR #5; contract+tsc+build+pytest |
| M3–M9 | ⬜ | Se KØREPLAN; alt blokeret af M2 |

## Important Files

- `docs/plans/m2-sidecar-v0.md` — teknisk design for M2 (læs FØR implementering)
- `lib/agent/contract.ts` + `sidecar/src/agent_sidecar/main.py` — kontraktens to sider
- `lib/agent/sidecarClient.ts` — swap-seamet

## Blockers

- Ingen tekniske. Åbne beslutninger (ikke-blokerende nu): LiveKit Scale-tier (2026-08-15), LICENSE (før distribution), GDPR-review (2026-09-01)

## Next Steps

1. #5 owner-scoping (x-tenant-id + registry, 403 + audit ved mismatch)
2. #6 struktur-split (contracts.py, routes/, runtime/) + AgentProfile-loader
3. M2-gate: qa-release-tjek (docs/qa/) med visuel /agent-demo-verifikation mod sidecar → M3 ∥ M4

## Notes

- Commit-beskeden "M2: Complete sidecar implementation" (`f3f4a77`) overdriver — stol på tickets, ikke commit-historik
- `.env.local` har sidecar-URL sat → sidecar-mode virker nu NÅR uvicorn kører på :8000; uden sidecar: fjern env-var for stub-mode
- Testnote: httpx ASGITransport buffer'er hele responsen — uendelige SSE-streams kan ikke integrationstestes den vej; brug komponent-tests eller rigtig server
