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
- #1 ✅ done · #4 ⏳ (workflow skrevet, afventer grøn GitHub-run) · næste: **#2 BFF SSE-proxy**

## Verified This Session

- **#1 DONE (verificeret)**: MeetingBus i sidecar; POST /agent/respond driver nu SSE-sekvensen med kommandoens correlationId/agentInstanceId; heartbeat; ingen replay ved reconnect. 19/19 pytest grønne
- DoD-brud 1 og 3 (sidecar-side) fra audit er lukket; brud 2 (BFF-proxy) = ticket #2
- `.github/workflows/ci.yml` skrevet (web: contract+tsc+build; sidecar: pytest); `tsc --noEmit` og `pnpm build` verificeret rene lokalt
- Docs merged til main via PR #6 (`d5779c0`); M2-branch rebased (`f3f4a77`)

## Status Overview

| Item | Status | Summary |
|------|--------|---------|
| M0 kontrakt | ✅ | Zod + schema + drift-test + BFF-ruter |
| M1 agent-kort | ✅ | Kun `/agent-demo`; tabletop = draft #7 |
| M2 sidecar | ⏳ | #1 ✅; #2 næste; #3 halvt (sidecar-side); #4 afventer CI-run |
| CI | ⏳ | Workflow skrevet; grøn run mangler |
| M3–M9 | ⬜ | Se KØREPLAN; alt blokeret af M2 |

## Important Files

- `docs/plans/m2-sidecar-v0.md` — teknisk design for M2 (læs FØR implementering)
- `lib/agent/contract.ts` + `sidecar/src/agent_sidecar/main.py` — kontraktens to sider
- `lib/agent/sidecarClient.ts` — swap-seamet

## Blockers

- Ingen tekniske. Åbne beslutninger (ikke-blokerende nu): LiveKit Scale-tier (2026-08-15), LICENSE (før distribution), GDPR-review (2026-09-01)

## Next Steps

1. Push + verificér CI grøn på GitHub → markér #4 ✅
2. #2 BFF SSE-proxy (design i `docs/plans/m2-sidecar-v0.md`) → lukker #3 E2E
3. #5 owner-scoping; #6 struktur-split + profile-loader
4. M2-gate: qa-release-tjek på /agent-demo mod sidecar → M3 ∥ M4

## Notes

- Commit-beskeden "M2: Complete sidecar implementation" (`f3f4a77`) overdriver — stol på tickets, ikke commit-historik
- `.env.local` har sidecar-URL sat → demo stadig brudt i sidecar-mode indtil #2 (BFF-proxy); stub-mode virker (fjern env-var)
- Testnote: httpx ASGITransport buffer'er hele responsen — uendelige SSE-streams kan ikke integrationstestes den vej; brug komponent-tests eller rigtig server
