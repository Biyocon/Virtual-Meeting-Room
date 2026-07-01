# Lessons

Durable rules from user corrections and hard-won discoveries.
Read this file at session start and apply it before touching code.

## How to use this file

- One rule per numbered line. Append-only: supersede with ~~strikethrough~~ + **RESOLVED [date]:**.
- Promote a lesson here when the user corrects workflow/process, or when a mistake burns real time.

## Rules

1. **A milestone is done only when its stage-3 §4 DoD-sentence is demonstrable — "code exists" is not done.**
**Why:** Commit "M2: Complete sidecar implementation" was ~40% real; respond/events were never coupled. A full re-audit was needed to discover it.
**How to apply:** Before marking any milestone ✅, run the demo/test that proves the DoD sentence, and fill a `docs/qa/` release check at milestone gates.

2. **Update `docs/KØREPLAN.md`/`docs/DEPS.md` in the same PR as the code that changes milestone state.**
**Why:** Planning docs drifted from code in under a week (KØREPLAN said "M0 AKTIV" while git was at M2), costing a full realignment.
**How to apply:** Any PR that starts/finishes a ticket edits the ticket status + KØREPLAN row + CHANGELOG entry.

3. **Verify assumed existing assets with Glob/ls before estimating — never from docs alone.**
**Why:** Stage-3 plan assumed Biyocon shipped `lib/livekit`, `lib/auth`, `useMeetingRealtime`, `components/tabletop/`; none exist. M6/M8 "reuse" estimates were actually greenfield.
**How to apply:** At planning time, list the directories/files the plan claims to reuse and confirm each exists.

4. **Contract changes touch three artifacts + two test suites.**
**Why:** The contract lives in `lib/agent/contract.ts`, `lib/agent/agent-event.schema.json`, AND the Pydantic mirror in `sidecar/.../main.py`; the drift guard only compares type-name sets, so payload drift slips through silently.
**How to apply:** Edit all three, then run `pnpm test:contract` AND `pytest sidecar/tests` before claiming done.

5. **Don't trust `pnpm build` green — `next.config.mjs` ignores TS and ESLint errors.**
**Why:** v0 scaffold defaults (`ignoreBuildErrors: true`) mask type errors; there is no CI yet.
**How to apply:** Run `tsc --noEmit` manually until tickets #4 (CI) and #8 (remove flags) land.
