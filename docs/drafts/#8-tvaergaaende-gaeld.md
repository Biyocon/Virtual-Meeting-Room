---
id: "#8"
title: "Tværgående teknisk gæld (v0-rester + config)"
milestone: "løbende"
status: draft
prioritet: "P2"
deps:
  - "#4"
blocks: []
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

v0-scaffoldets defaults skjuler fejl og forvirrer: builds ignorerer TS/ESLint-fejl, sidecar-URL eksponeres unødigt i klient-bundle, projektnavn er stadig `my-v0-project`. Ufarligt enkeltvis — samlet underminerer det CI-gaten (#4) og distribution (LICENSE).

## Done ser sådan ud

Build fejler på typefejl. Ingen v0-rester i config. LICENSE afklaret.

## Teknisk scope

- [ ] `next.config.mjs`: fjern `ignoreBuildErrors` + `ignoreDuringBuilds` (KRÆVER #4 grøn først — fix afslørede typefejl)
- [ ] `NEXT_PUBLIC_AGENT_SIDECAR_URL` → `AGENT_SIDECAR_URL` (server-only; koordinér med #2)
- [ ] `package.json` name → `virtual-meeting-room`
- [ ] Slet `.pr-body-tmp.md`, `tsconfig.tsbuildinfo` fra tree; tjek `.gitignore` dækker `sidecar/.pytest_cache`, `*.tsbuildinfo`
- [ ] `AI_Meeting_Room_PRD_v1.0.md` (rod) → flyt til `docs/architecture/` som historisk kilde eller slet (PRD v1.2 i docs/ er autoritativ)
- [ ] LICENSE-beslutning (ADR-0001-blocker) — kræver ejer-input
- [ ] Broad `except Exception → 400` i sidecar-respond → skel klient- fra serverfejl (400 vs 500)

## Acceptkriterie

- [ ] `pnpm build` fejler ved bevidst typefejl
- [ ] `grep -r NEXT_PUBLIC_AGENT` tom
- [ ] Repo-rod uden stray-filer
- [ ] LICENSE-fil findes eller beslutning dokumenteret i CHANGELOG

## Blocker / noter

2026-07-01: LICENSE kræver menneskelig beslutning — flag ved M2-gate-review.
