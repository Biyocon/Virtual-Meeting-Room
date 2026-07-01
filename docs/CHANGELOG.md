# Changelog: Virtual Meeting Room (VMR)
**Ref:** `docs/DEPS.md` (change-impact procedure) | `docs/PRD.md`

<!--
HVAD LOGGES HER:
  ✅ Ændringer til PRD.md (nye/fjernede/ændrede krav)
  ✅ Ændringer til KØREPLAN.md (nye faser, re-sekvensering, scope-beslutninger)
  ✅ Ændringer til DEPS.md (nye blokerings-relationer)
  ✅ Prioritetsændringer (P0 → P1, ny P0 tilføjet)

HVAD LOGGES IKKE HER:
  ❌ Kodeændringer — det hører i git commit-beskeder
  ❌ Test-resultater — det hører i docs/qa/
  ❌ Audit-findings — det hører i docs/audit/

ARKIVERING: Når filen nærmer sig 20 entries, arkivér de ældste til
docs/plans/changelog-arkiv-2026.md og behold kun de seneste 10 her.
-->

---

## Aktive entries

### [2026-07-01] Modifikation: Docs-drift-audit + komplet system-realignment

**Type:** modifikation
**Ændrede filer:** PRD.md (v1.2), KØREPLAN.md (rewrite), DEPS.md (rewrite), CHANGELOG.md (ny), LESSON.md (ny), docs/active/ (6 tickets), docs/drafts/ (2 tickets), docs/done/ (2 tickets), docs/plans/m2-sidecar-v0.md, CLAUDE.md, primer.md, AGENTS.md, tasks/lessons.md, README.md
**Årsag:** Kodebase-audit viste at KØREPLAN var driftet ift. både stage-3-planen og faktisk kode: M0 stod som "AKTIV" mens git var på M2; milestone-definitioner matchede ikke stage-3 §1; commit-besked "M2: Complete" overdrev (~40% reelt, DoD ikke opfyldt)
**Berørte tasks:** Alle — ny ticket-nedbrydning #1–#8 erstatter gammel M0-1…M2-4-nummerering
**Impact:**
- M0, M1: markeret ✅ done (commit `93d60f1`); M1 tabletop-integration udskilt som draft #7
- M2: re-defineret pr. stage-3 DoD ("swap uden UI-ændring"); 6 tickets oprettet (#1–#6)
- M6, M8: estimater hævet — planlagt "genbrug af Biyocon-assets" (lib/livekit, useMeetingRealtime m.fl.) findes ikke i repo → greenfield
- Kritisk sti opdateret: alt går gennem M2
**Beslutning krævet:** Nej (statusrettelse, ikke scope-ændring). Åbne beslutninger uændret i PRD §8.

### [2026-06-28] Initial: Planlægningssystem oprettet

**Type:** tilføjelse
**Ændrede filer:** PRD.md, KØREPLAN.md, DEPS.md
**Årsag:** Projekt oprettet — baseline etableret fra ADR 0001–0006
**Berørte tasks:** Alle
**Impact:** Ingen re-sekvensering nødvendig (ny baseline)
**Beslutning krævet:** Nej

---

<!--
ENTRY-FORMAT (kopiér ved ny entry):

### [YYYY-MM-DD] Ændring: <kort titel>

**Type:** tilføjelse | fjernelse | modifikation | prioritetsændring
**Ændrede filer:** <liste>
**Årsag:** <1 sætning — HVORFOR>
**Berørte tasks:** #N, #M, Milestone X
**Impact:**
- #N: re-sekvenseret (blokeres nu af #M)
**Beslutning krævet:** ja — <hvad og af hvem> | nej
-->
