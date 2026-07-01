---
id: "#4"
title: "CI: contract-test + pytest på hver PR"
milestone: "M2"
status: active
prioritet: "P0"
deps: []
blocks:
  - "#8"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

`lib/agent/contract.ts` påstår "scripts/agent-contract.test.mjs fails CI on drift" — men der findes ingen `.github/`-mappe. Hverken drift-guard eller pytest kører automatisk. Kontrakt-drift mellem TS og Python opdages i dag kun manuelt. Isoleret task uden deps — kan starte straks, parallelt med #1.

## Done ser sådan ud

Enhver PR mod main kører automatisk: TS contract-test, sidecar-pytest, typecheck og build. Rød CI blokerer merge.

## Teknisk scope

- [ ] `.github/workflows/ci.yml`: pnpm install → `pnpm test:contract` → `tsc --noEmit` → `pnpm build`
- [ ] Python-job: `pip install -e ./sidecar[dev]` → `pytest sidecar/tests`
- [ ] Branch protection-note i CONTRIBUTING/README (manuel GitHub-indstilling)
- [ ] Cache pnpm + pip for hastighed

## Relevante filer

- `scripts/agent-contract.test.mjs`
- `sidecar/pyproject.toml` (dev-extras)
- `package.json` (scripts: `test:contract`)

## Acceptkriterie

- [ ] CI kører grønt på nuværende branch
- [ ] Bevidst kontrakt-brud (ekstra event-type i schema) → CI rød
- [ ] pytest-fejl → CI rød
- [ ] Køretid < 5 min

## Blocker / noter

2026-07-01: OBS — `tsc --noEmit` kan afsløre eksisterende typefejl skjult af `ignoreBuildErrors: true`. Fix dem her, eller start med typecheck som non-blocking og stram til i #8.
