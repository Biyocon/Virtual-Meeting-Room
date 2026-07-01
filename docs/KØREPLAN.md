# Køreplan: Virtual Meeting Room (VMR)
**Oprettet:** 2026-06-28
**Opdateret:** 2026-07-01
**Ref:** `docs/PRD.md` | `docs/DEPS.md` | `docs/architecture/stage-3-build-execution-plan.md`

<!--
HÅRDT LOFT: Denne fil må IKKE overskride 200 linjer.
Detaljer hører til i docs/active/, docs/drafts/ og docs/plans/.
Når en milestone er done: marker ✅ + dato + commit-hash. Arkivér ikke.
Milestone-definitionerne følger stage-3-build-execution-plan.md — IKKE tidligere drift-versioner.
-->

---

## Overblik

| Milestone | Navn | Status | Gate |
|-----------|------|--------|------|
| M0 | Agent Event Contract + skeleton | ✅ KOMPLET (commit `93d60f1`, PR #4) | `agent.status` flyder UI ← BFF ← stub via SSE |
| M1 | Én talende agent-kort | ✅ KOMPLET som isoleret demo (`/agent-demo`) | Kort viser 4 states + streamet tekst + disclosure |
| M2 | Sidecar v0 (swap uden UI-ændring) | ⏳ AKTIV (~40%) | TS-stub byttes til sidecar UDEN UI-ændring |
| M3 | Azure TTS-pipeline | ⬜ PLANLAGT | Agent-svar afspilles som Azure-stemme, p99 < 1.5s |
| M4 | Whisper STT-stub | ⬜ PLANLAGT | Transskript påvirker agent-svar; usage auditeret |
| M5 | KnowledgeScope RAG v0 | ⬜ PLANLAGT | Svar indeholder min. 1 citation fra uploadet fil |
| M6 | LiveKit live media | ⬜ PLANLAGT | Menneske + agent-audio i samme LiveKit-rum |
| M7 | Møde-opsummering | ⬜ PLANLAGT | Summary + beslutninger + action items eksporterbar |
| M8 | Teams-ready + M365 | ⬜ PLANLAGT | Agent læser 1 SharePoint-kilde i Teams-møde, auditeret |
| M9 | Enterprise self-host | ⬜ PLANLAGT | Samme app kører self-hosted EU/DK uden frontend-rewrite |

---

## Milestone M0 — Agent Event Contract + Skeleton ✅

**Afsluttet:** commit `93d60f1` (PR #4)
**Leveret:** `lib/agent/contract.ts` (Zod, 8 events + 4 commands, OwnerScope), `lib/agent/agent-event.schema.json` (sprogneutralt spejl), BFF-ruter (`app/api/agent/respond`, `app/api/agent/events/[meetingId]` SSE), in-memory bus (`lib/agent/bus.ts`, dev-only), audit-stub, swap-seam (`lib/agent/sidecarClient.ts`), contract-drift-test (`pnpm test:contract`).
**Afvigelse fra plan:** Pydantic-kontrakt ligger inline i `sidecar/src/agent_sidecar/main.py` — ikke separat `contracts.py`. Rettes i M2 (ticket #6).

---

## Milestone M1 — Én Talende Agent-kort ✅ (isoleret demo)

**Afsluttet:** commit `93d60f1` (PR #4)
**Leveret:** `components/agent-card.tsx` (4 states, waveform, streaming-cursor, altid-synligt "Syntetisk stemme"-badge), `hooks/useAgentEvents.ts` (EventSource, correlationId-dedup), `app/agent-demo/page.tsx`, `lib/agent/stub.ts`.

**Kendte restmangler (accepteret — flyttet til drafts):**
- Kortet er IKKE integreret i tabletop-UI — `app/page.tsx` er stadig statisk v0-mockup → ticket #7 (drafts)
- Status-debounce (M1-risiko-mitigering) ikke implementeret → del af ticket #7

---

## Milestone M2 — Sidecar v0 ⏳ AKTIV

**Mål:** TS-stub byttes til Python-sidecar uden UI-ændring (DoD stage-3 §4)
**Blokkeret af:** M0 ✅
**Blokerer:** M3, M4, M5
**Status:** Scaffold + Pydantic-spejl + tests findes. DoD IKKE opfyldt — 3 konkrete brud (se tickets #1–#3).

| Ticket | Opgave | Status | Acceptkriterie |
|--------|--------|--------|----------------|
| #1 | Sidecar-intern event-kobling: `/agent/respond` driver SSE-stream | ✅ 2026-07-02 | POST respond → delta→final på `GET /agent/events/{meetingId}` |
| #2 | BFF SSE-proxy af sidecar-stream (bus omgås når sidecar-URL sat) | ⬜ | UI modtager sidecar-events via eksisterende BFF-endpoint uændret |
| #3 | Ægte `agentInstanceId`/`correlationId` propageres end-to-end | ⏳ sidecar-side ✅ i #1; E2E-verifikation afventer #2 | Demo-kortets events matcher; ingen hardcoded `agent-0` |
| #4 | CI: `test:contract` + pytest på hver PR | ⏳ workflow skrevet; afventer grøn run | GitHub Actions rød ved kontrakt-drift eller test-fejl |
| #5 | Owner-scoping på events-endpoint | ⬜ | Forkert tenantId afvises (testplan §6 scoping-test) |
| #6 | AgentProfile-loader (custom-format) + `contracts.py` udskilles | ⬜ | 3+ profiler loader; ugyldig profil fejler; struktur pr. stage-3 §5 |

**Milestone-gate:** Demo på `/agent-demo` kører mod sidecar med `AGENT_SIDECAR_URL` sat, alle events ægte, CI grøn → M3+M4 kan starte parallelt. Verificér med `docs/qa/`-release-tjek.

---

## Milestone M3 — Azure TTS Pipeline

**Mål:** Agent taler med Azure Neural Voice (EU), latency under krav
**Blokkeret af:** M2 komplet · **Blokerer:** M6

| Sprint | Opgave | Status | Acceptkriterie |
|--------|--------|--------|----------------|
| M3-1 | `adapters/tts_azure.py` — adapter-baseret (ADR-0004) | ⬜ | TTS-kald lykkes mod EU-endpoint; provider swappable |
| M3-2 | `agent.audio`-event + client-afspilning | ⬜ | Browser modtager `agent.audio` og afspiller lyd |
| M3-3 | Retention/cache-regler for TTS-artefakter | ⬜ | Slette-regler dokumenteret + implementeret fra start (ADR-0004) |
| M3-4 | Latency-benchmark | ⬜ | p99 < 1.5s (LLM-svar → lyd i browser) |

---

## Milestone M4 — Whisper STT

**Mål:** Menneskelig tale → transskript → sidecar-kontekst, auditeret
**Blokkeret af:** M2 komplet · **Blokerer:** M6

| Sprint | Opgave | Status | Acceptkriterie |
|--------|--------|--------|----------------|
| M4-1 | `adapters/stt_whisper.py` (Azure-hosted) | ⬜ | Transskription < 800ms efter tale-slut |
| M4-2 | Transskript ind i agent-kontekst | ⬜ | Transskript påvirker agent-svar demonstrérbart |
| M4-3 | STT-usage audit-events | ⬜ | Al STT-brug producerer `audit.event` |

---

## Milestone M5 — KnowledgeScope RAG v0

**Mål:** Agent citerer kildefiler i svar
**Blokkeret af:** M1 + M2 komplet · **Blokerer:** M7

| Sprint | Opgave | Status | Acceptkriterie |
|--------|--------|--------|----------------|
| M5-1 | Fil-upload + retrieval (`runtime/rag.py`) | ⬜ | 1 uploadet fil kan retrieves |
| M5-2 | Citations i `agent.message.final` | ⬜ | Min. 1 citation; UI viser klikbar citation-chip |
| M5-3 | Citation-rate logging | ⬜ | ≥ 80% af svar har citation (PRD §6) |

---

## Milestones M6–M9 (planlagt — detaljeres når blokkere er løst)

| MS | Kerneleverance | Blokkeret af | Kritisk forudsætning |
|----|----------------|--------------|----------------------|
| M6 | LiveKit-rum: menneske-tracks + agent publicerer audio-track | M1, M3, M4 | **OBS: ingen LiveKit-kode/deps i repo — greenfield, ikke "genbrug"** (se LESSON.md). Scale-tier-beslutning 2026-08-15 |
| M7 | `meeting.summary`, beslutningslog, action items, eksport | M5 | RAG-kvalitet |
| M8 | Entra-auth, Teams-sidepanel, scoped Graph via `FileAccessGrant` | M6, M7 | Legal/Graph-permissions (frist 2026-09-01) |
| M9 | Self-host LiveKit + Azure-containere, tenant-isolation, admin/audit-dashboard | M8 | LICENSE-afklaring (ADR-0001-blocker) |

---

## Tværgående gæld (uafhængig af milestones — ticket #8, drafts)

- `next.config.mjs`: `ignoreBuildErrors` + `ignoreDuringBuilds` fjernes når CI (#4) er grøn
- `NEXT_PUBLIC_AGENT_SIDECAR_URL` → server-only `AGENT_SIDECAR_URL`
- Pydantic v1-style `class Config` → `model_config = ConfigDict(...)`
- `package.json` name `my-v0-project` → `virtual-meeting-room`; README udbygget
- Ingen LICENSE-fil (ADR-0001: blocker før distribution)
- Ingen tests af TS-runtime-sti (BFF-ruter, hook, kort) — testplan §6 integration/UI/scoping/reconnect

---

## Deferred

| Punkt | Årsag | Revurderes |
|-------|-------|------------|
| LiveKit Scale-tier EU-pinning | $500/md — afventer produktejer | 2026-08-15 eller M6-start |
| Model Lab Council/Compare (ADR-0006) | Efter M2; Council først; pattern-only reimplementation | M2 done |
| Voice cloning (M9+) | GDPR consent-flow + CnV-godkendelse | M8 done |
| AR/VR møderum | Ingen dokumenteret efterspørgsel | Post-M9 |
| Mobiloptimering | Desktop-first i MVP | M7–M8 |

---

## Arkiv

- 2026-07-01: Oprindelig KØREPLAN-milestone-nedbrydning (M2 = "AgentProfile loader", kontrakt i `types/events.ts`) arkiveret — var driftet ift. stage-3-planen og faktisk kode. Denne version følger stage-3 §1.
