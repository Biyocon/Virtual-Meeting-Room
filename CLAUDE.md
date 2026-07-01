# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and other coding
agents when working in this repository. **These instructions override default
behavior — follow them exactly.**

---

# Virtual Meeting Room (VMR)

AI-drevet virtuelt møderum hvor AI-agenter med syntetisk stemme sidder ved bordet som ligestillede, tydeligt mærkede deltagere.

## Source-of-truth order

When sources conflict, trust them in this order:

```
code > primer.md > docs/KØREPLAN.md > tasks/lessons.md > CLAUDE.md
```

ADRs (`docs/adr/0001–0006`) are immutable decisions — never override them; a new architecture decision requires a new ADR.

## Session Memory Workflow

At the start of every session, read in order: `primer.md` → `tasks/lessons.md`. Apply lessons as durable operating rules. At the end of the session, **rewrite `primer.md` completely** (current focus, done, in progress, blockers, next steps).

## Planning Documents (docs/ — managed via /codesprint)

| File | Answers |
|---|---|
| `docs/PRD.md` | What are we building and why? (features P0–P2, metrics) |
| `docs/KØREPLAN.md` | What now, in what order? (milestones M0–M9, ≤200 lines) |
| `docs/DEPS.md` | What blocks what? (critical path, change-impact procedure) |
| `docs/active/#N-*.md` | Current tickets with acceptance criteria |
| `docs/CHANGELOG.md` | Planning changes (NOT code changes — those live in git) |

**Never read all of KØREPLAN/PRD at session start** — primer.md is the condensate. Any change to PRD/KØREPLAN/tickets must run the change-impact procedure in `docs/DEPS.md` and log to `docs/CHANGELOG.md`. Docs update in the SAME PR as the code they describe.

---

## Commands

```bash
pnpm dev              # Next.js dev server
pnpm build            # Production build (currently ignores TS errors — see gotchas)
pnpm test:contract    # TS ↔ JSON-schema contract drift guard

# Sidecar (Python 3.11+, from sidecar/)
pip install -e ".[dev]"
python -m uvicorn agent_sidecar.main:app --reload --port 8000
pytest tests/
```

Path alias: `@/*` maps to repo root.

---

## Architecture

```
app/
  agent-demo/page.tsx        # Working M1 demo (isolated) — the E2E test surface
  api/agent/respond/         # BFF: validates AgentCommand, audits, 202
  api/agent/events/[meetingId]/  # BFF: SSE stream (heartbeat 15s)
  page.tsx                   # STATIC v0 mockup — not wired to anything (ticket #7)
lib/agent/
  contract.ts                # Zod contract: 8 events + 4 commands (SOURCE OF TRUTH)
  agent-event.schema.json    # Language-neutral mirror (drift-guarded)
  bus.ts                     # In-memory dev-only event bus
  sidecarClient.ts           # AgentRuntime swap seam: stub vs HTTP sidecar
  stub.ts                    # TS mock runtime
components/agent-card.tsx    # 4 speaking-states + mandatory disclosure badge
hooks/useAgentEvents.ts      # EventSource → AgentView reducer, correlationId dedup
sidecar/src/agent_sidecar/main.py  # FastAPI + Pydantic contract mirror
docs/                        # Planning system (PRD, KØREPLAN, DEPS, tickets, ADRs)
```

### Dataflow (target M2)

```
UI (useAgentEvents) ← SSE ← BFF /api/agent/events ← proxy ← sidecar SSE
UI action → BFF /api/agent/respond → sidecarClient → sidecar POST /agent/respond → sidecar bus
```

---

## Key Gotchas

- **`app/page.tsx` is a dead v0 mockup** — the real demo is `/agent-demo`. Don't "fix" the mockup; ticket #7 replaces it.
- **`next.config.mjs` ignores TS + ESLint build errors** — `pnpm build` green ≠ type-safe. Run `tsc --noEmit` yourself until #8 removes the flags.
- **Contract changes require BOTH sides + schema**: `lib/agent/contract.ts`, `agent-event.schema.json`, and the Pydantic mirror in `sidecar/.../main.py` — then `pnpm test:contract` + pytest.
- **The in-memory bus (`lib/agent/bus.ts`) is single-process dev-only** — don't build multi-process features on it.
- **Sidecar respond/events are NOT yet coupled** (tickets #1–#3): enabling `NEXT_PUBLIC_AGENT_SIDECAR_URL` currently breaks the demo end-to-end.
- **Disclosure badge ("Syntetisk stemme") must never get a disable prop** (ADR-0004, PRD P0).
- **All events require OwnerScope** (`tenantId` + `meetingId`); `dataClassification` is `"test_only"` until further notice (ADR-0003).
- **No LiveKit code exists in this repo** despite docs implying reuse — M6 is greenfield.
- **KØREPLAN.md hard cap: 200 lines.** Details go to `docs/active/`, `docs/plans/`.

---

## Code Style

- **UI language:** Danish (labels, badges). **Code language:** English (identifiers, comments, commits).
- Tailwind CSS v4 + shadcn/ui; components in `components/ui/` are generated — don't hand-edit.
- Zod for all BFF input validation; Pydantic v2 style (`model_config = ConfigDict(...)`) in sidecar.
- Package manager: **pnpm** (canonical — never npm/yarn).

---

## Agent Conventions

- Confirm hard-to-reverse / outward-facing actions before doing them.
- Commit or push only when asked. PR-per-milestone-ticket; branch off `main`.
- A milestone is done ONLY when its DoD from `docs/architecture/stage-3-build-execution-plan.md` §4 is demonstrable — "code exists" is not done (see LESSON.md).
- Run `pnpm test:contract` + `tsc --noEmit` + sidecar pytest before claiming any contract-touching task complete.
