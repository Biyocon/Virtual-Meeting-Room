---
id: "#9"
title: "M2-gate: qa-release-tjek + merge af PR #5"
milestone: "M2"
status: draft
prioritet: "P0"
deps:
  - "#5"
  - "#6"
blocks:
  - "M3"
  - "M4"
oprettet: "2026-07-02"
sidst_opdateret: "2026-07-02"
---

## Hvad & Hvorfor

M2 må kun markeres ✅ når DoD-sætningen er demonstrérbar og verificeret via qa-release-tjek (lesson #1: "code exists" ≠ done). Denne ticket ER gaten: den samler verifikationen, godkender og merger PR #5.

## Done ser sådan ud

`docs/qa/release-2026-MM-DD.md` udfyldt og GODKENDT; PR #5 merged til main; M2 markeret ✅ i KØREPLAN med commit-hash; M3 + M4 kan startes.

## Teknisk scope

- [ ] Kopiér `~/.claude/templates/docs/qa/_RELEASE.md` → `docs/qa/release-YYYY-MM-DD.md`
- [ ] Build/typecheck/tests-sektion: CI-run-link + `pnpm test:contract` + pytest lokalt
- [ ] Kritiske flows (manuel, i browser): `/agent-demo` mod kørende sidecar — alle 4 states synlige, streamet tekst, disclosure-badge; stub-mode regression (uden env-var)
- [ ] Fejlflow: sidecar nede → UI fejler synligt, ingen hængende spinner
- [ ] Scoping-flow: forkert tenantId → 403 (leveres af #5)
- [ ] LESSON.md: M2-lesson skrives (fase-afslutning)
- [ ] KØREPLAN: M2 → ✅ + dato + merge-hash; DEPS: M3/M4 afblokeres
- [ ] Merge PR #5 (squash), slet branch, rebase-tjek af evt. åbne branches

## Relevante filer

- `docs/plans/m2-sidecar-v0.md` (DoD-liste)
- `docs/qa/` (tom — første release-tjek)
- PR #5: https://github.com/Biyocon/Virtual-Meeting-Room/pull/5

## Acceptkriterie

- [ ] Alle "Kritisk"-punkter i release-tjekket er ✅
- [ ] Visuel browser-verifikation af /agent-demo mod sidecar dokumenteret (screenshot i docs/screenshot/)
- [ ] PR #5 merged; CI grøn på main
- [ ] M2-lesson skrevet i LESSON.md

## Blocker / noter

2026-07-02: Oprettet som draft — aktiveres når #5 + #6 er done. Curl-baseret E2E er allerede verificeret (#2); gaten tilføjer den visuelle/manuelle del.
