# Dependency Map: Virtual Meeting Room (VMR)
**Opdateret:** 2026-07-01
**Ref:** `docs/KØREPLAN.md` | `docs/PRD.md` | `docs/adr/0001–0006`

<!--
Dette er change-impact-systemets hjerne.
Opdateres ALTID når:
  - En ny milestone/ticket oprettes
  - En milestone flyttes til done
  - En PRD-ændring sker (kør change-impact-procedure nedenfor)

Tommelfingerregel: Hvis du ikke kan se konsekvensen af en ændring
ved at læse DEPS.md, er DEPS.md forældet.
-->

---

## Milestone-blokerings-relationer

| Milestone | Blokeres af | Blokerer | Note |
|-----------|-------------|----------|------|
| **M0** — Agent Event Contract | _(ingen)_ | M1, M2 | ✅ done — blokerer ikke længere noget |
| **M1** — Agent-kort UI | M0 ✅ | M5, M6, M7 | ✅ done som demo; tabletop-integration (#7) er IKKE en bloker for M5 |
| **M2** — Sidecar v0 | M0 ✅ | M3, M4, M5 | ⏳ AKTIV — eneste aktive bloker i systemet |
| **M3** — Azure TTS | M2 | M6 | TTS forudsætning for agent-som-audio-deltager |
| **M4** — Whisper STT | M2 | M6 | STT forudsætning for agent-som-lyttende-deltager |
| **M5** — KnowledgeScope RAG v0 | M1 ✅, M2 | M7 | Kræver UI (citations) + sidecar (retrieval) |
| **M6** — LiveKit live media | M1 ✅, M3, M4 | M8 | **Greenfield** — ingen LiveKit-kode findes i repo |
| **M7** — Møde-opsummering | M5 | M8 | Opsummering kræver RAG-kvalitet |
| **M8** — Teams + M365 | M6, M7 | M9 | Kræver Legal/Graph-permissions (ekstern) |
| **M9** — Enterprise self-host | M8 | _(ingen)_ | Slutpunkt; kræver LICENSE-afklaring |

---

## Kritisk sti

**Kritisk sti (minimum tid til M9):**

```
M2 (⏳) → M3 → M6 → M8 → M9
```

**Alternativ sti (content-stack):**

```
M2 (⏳) → M5 → M7 → M8 → M9
```

Begge stier konvergerer ved M8. **Alt går gennem M2 — færdiggørelse af M2 er den højeste prioritet i hele projektet.**

**Estimeret minimumstid:** 5–7 måneder fra M2-done (M6 og M8 er større end oprindeligt estimeret, da "genbrug af Biyocon-assets" viste sig at være greenfield — se LESSON.md).

---

## Ticket-niveau blokerings-relationer (M2 — aktive tickets)

| Ticket | Blokeres af | Blokerer | Note |
|--------|-------------|----------|------|
| #1: Sidecar respond→events-kobling | _(ingen)_ | #2, #3, M2-gate | Kernen i DoD; sidecar-intern meeting-scoped bus |
| #2: BFF SSE-proxy | #1 | #3, #5, M2-gate | UI må ikke ændres — proxy bag eksisterende endpoint |
| #3: agentInstanceId/correlationId propagation | #1, #2 | M2-gate | Fjern hardcoded `agent-0` |
| #4: CI (test:contract + pytest) | _(ingen)_ | M2-gate, gæld #8 | Isoleret — kan starte NU parallelt med #1 |
| #5: Owner-scoping på events | #2 | M2-gate | Testplan §6 scoping-test |
| #6: AgentProfile-loader + contracts.py | #1 | M3-1, M4-1, M5-1 | Struktur pr. stage-3 §5; kan starte efter #1 |
| #7 (draft): Tabletop-integration af AgentCard | M2-gate | M6-UI | Bevidst udskudt — demo er nok til M2-verifikation |
| #8 (draft): Tværgående gæld | #4 (CI først) | _(ingen)_ | ignoreBuildErrors må først fjernes når CI fanger fejl |

---

## Paralleliseringsmuligheder

| Parallel gruppe | Forudsætning | Gevinst |
|-----------------|--------------|---------|
| **#1 ∥ #4** | _(ingen)_ | CI-gate klar samtidig med kernearbejdet |
| **#5 ∥ #3** | #2 done | Scoping og ID-propagation rører forskellige lag |
| **M3 ∥ M4** | M2 done | Uafhængige Azure-integrationer |
| **M6 ∥ M7** | (M3+M4) ∥ M5 | Separate blokerings-stier |

**Anbefalet rækkefølge i praksis:**
1. Start #1 og #4 parallelt (i dag)
2. #2 når #1 er done → #3 og #5 parallelt
3. #6 parallelt med #2/#3 (efter #1)
4. M2-gate: alle tickets ✅ + qa-release-tjek → start M3 ∥ M4
5. M5 når M2 done → M7; M6 når M3+M4 done

---

## Isolerede tasks

Uden afhængigheder til aktive milestones — prioritér ved ledig kapacitet:

- **#4 CI-pipeline** — ingen deps; størst risikoreduktion pr. time
- **Avatar-portræt-sæt** (illustreret stil, `docs/design/avatar-style-spec.md`) — kan commissioneres straks
- **LICENSE-afklaring** (ADR-0001) — ren beslutning, ingen kode
- **Legal review** (GDPR + syntetisk stemme EU) — afventer juridisk ressource
- **LLM Benchmark / Model Lab manuel fase** (ADR-0006) — parallelt med M2+

---

## Åbne afhængigheder

| Afhængighed | Afventer | Frist |
|-------------|----------|-------|
| M6 EU-latency → LiveKit Scale-tier ($500/md) | Produktejer-beslutning | 2026-08-15 |
| M8 Teams-bot → Microsoft Graph-permissions | Legal + Microsoft-partner-godkendelse | 2026-09-01 |
| M9 Voice cloning (CnV) → Azure-godkendelse | Azure-ansøgning + GDPR consent-flow | M8 done |
| Distribution → LICENSE-fil mangler | Ejer-beslutning (ADR-0001) | Før første eksterne release |

---

## Change-Impact Procedure

Kør denne procedure ved ENHVER ændring til PRD, KØREPLAN eller milestones:

```
GIVEN: Ændring [C] til [fil] på [dato]

1. KLASSIFICER:
   Type: tilføjelse | fjernelse | modifikation | prioritetsændring
   Omfang: PRD-niveau | milestone-niveau | ticket-niveau

2. QUERY DEPS.md (denne fil):
   - Find alle milestones/tickets der blokeres af det ændrede
   - Find alle tickets i samme milestone/sprint

3. VURDER per berørt milestone/ticket:
   - Re-sekvensering nødvendig? (ja/nej + begrundelse)
   - Acceptkriterie skal opdateres? (ja/nej + forslag)
   - Ticket nu irrelevant? (flyt til docs/drafts/ med note)
   - Ny bloker opstået? (opdater tabellerne ovenfor)

4. OPDATER:
   - docs/PRD.md (den ændrede sektion + version-bump)
   - docs/KØREPLAN.md (milestone-status + estimat)
   - Berørte tickets: tilføj [REVIEW: årsag · dato] i ticket-header
   - docs/DEPS.md (nye/fjernede relationer)
   - docs/CHANGELOG.md (entry med alle berørte milestones/tickets)

5. RAPPORTÉR:
   "X milestones/tickets påvirket. Y kræver review. Z kan fortsætte."
   List [REVIEW]-markerede tickets.
   Angiv hvad der kræver menneskelig beslutning.
```

**Husk:** ADR'er (0001–0006) ændres ALDRIG via change-impact-procedure.
Ny arkitektur-beslutning → ny ADR med eksplicit begrundelse.
