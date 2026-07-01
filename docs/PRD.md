# PRD: Virtual Meeting Room (VMR)
**Version:** 1.2
**Oprettet:** 2026-06-28
**Opdateret:** 2026-07-01
**Status:** AKTIV
**Ref:** `docs/KØREPLAN.md` | `docs/DEPS.md` | `docs/adr/0001–0006`

<!--
STATUS-værdier: DRAFT → AKTIV → FROSSEN → ARKIVERET
Frys kun PRD med eksplicit beslutning — skriv begrundelse i CHANGELOG.md.
Opdater version-nr. (1.0 → 1.1) ved enhver ændring til §1–§5.
ADR-beslutninger låser tech-stack-valg og må ikke overskrives herfra.
-->

---

## §1 Problem

Videomøder med mange deltagere taber vigtig kontekst, baggrundsviden og beslutningssporing. Mødedeltagere bruger uforholdsmæssig tid på at søge information under mødet frem for at træffe beslutninger. Eksisterende mødeplatforme (Teams, Zoom) understøtter ikke AI-agenter som ligestillede, kontekstbevidste deltagere.

**Hvem har problemet:** Vidensarbejdere i møder med specialistbehov (analytikere, projektledere, strategiteams)  
**Hyppighed:** Dagligt — typisk 2–5 møder per dag per person  
**Nuværende workaround:** Søger manuelt i interne systemer under mødet, spørger kollegaer, noter samles manuelt efter mødet

---

## §2 Løsning

VMR er et AI-drevet virtuelt møderum hvor "digitale medarbejdere" (AI-agenter med syntetisk stemme) sidder ved bordet som ligestillede deltagere. Agenter er forsynet med KnowledgeScope (adgang til relevante filer/systemer), taler via Azure Neural TTS, lytter via Whisper STT, og er tydeligt mærkede som AI via disclosure-badge.

Mødedeltagere kan stille spørgsmål direkte til AI-agenter — og modtage svar med kildehenvisninger — uden at forlade møderummet. Agenter kan sammenlignes og evalueres via Model Lab (ADR-0006).

**Kerneværdi:** AI-agenter som realtids-kollegaer ved mødebordet — ikke chatbots i et separat vindue

---

## §3 Personas

| Persona | Rolle | Smertepunkt | Mål med VMR | Betalingsvilje |
|---------|-------|-------------|-------------|----------------|
| **Amira** | Senior Projektleder | Bruger 30+ min/møde på at søge status i JIRA/Confluence | AI-facilitator opsummerer status i realtid ved mødestart | 500–1.000 DKK/md |
| **Jonas** | Strategisk Analytiker | Beslutningsgrundlag mangler i møder — data er i systemer, ikke i rummet | AI-analytiker trækker data og præsenterer ved bordet | 800–1.200 DKK/md |
| **Pia** | IT-ansvarlig / Compliance | Bekymret for GDPR, AI-transparens og kontrollerbarhed | VMR giver fuldt audit-log og klar disclosure af AI-status | 1.500–3.000 DKK/md (enterprise) |
| **Tobias** | Nye medarbejder | Mangler kontekst i møder — ved ikke hvem der ved hvad | AI-vidensstyring svarer på "hvad er baggrunden for X?" | 200–400 DKK/md |

---

## §4 Features

<!--
P0 = MVP (ingen lancering uden dette)
P1 = Vigtig (v1.x inden for 3 måneder efter MVP)
P2 = Ønskelig (fremtidig version)
Hvert acceptkriterie er et ja/nej-spørgsmål.
-->

### P0 — Kritisk (MVP)

| Feature | Beskrivelse | Acceptkriterie |
|---------|-------------|----------------|
| AgentCard med avatar | 2D illustreret portræt, semi-flat, 1:1 format | Agent-kort renderer korrekt avatar med navn, rolle og colorAccent på 1440px desktop |
| Speaking-state visualisering | idle / listening / thinking / speaking med visuelt feedback | Status-skift fra idle → speaking vises inden 500ms efter `agent.status`-event modtages |
| Tabletop-layout | 6–8 pladser rundt om digitalt bord | Minimum 4 agent-kort placeret rundt om bord-element på 1440px desktop |
| SyntheticVoiceBadge | "Digital medarbejder · syntetisk stemme" badge | Badge synlig på ALLE agent-kort; ingen prop til at slå fra |
| Agent Event Contract | BFF ↔ sidecar kommunikation via WS/SSE | `agent.status`-event opdaterer UI-tilstand inden 500ms; events er typet med `AgentEvent<T>` |
| Python sidecar stub (M2) | FastAPI sidecar returnerer mock AgentEvents | `POST /agent/respond` returnerer valid `AgentEvent` inden 2s |
| Meeting Controls | Mic, kamera, forlad, agent-panel toggle | Forlad-knap viser `AlertDialog`-bekræftelse; tab-navigation fungerer |

### P1 — Vigtig (v1 — inden 3 måneder efter MVP)

| Feature | Beskrivelse | Acceptkriterie |
|---------|-------------|----------------|
| Azure Neural TTS (M3) | Agent taler med Azure-syntetisk stemme | Stemme-latency < 1.5s fra LLM-svar til lyd i browser; EU-region enforced |
| Whisper STT (M4) | Menneskelig tale transskriberes | Transskription klar inden 800ms forsinkelse; tekst vises i chat-panel |
| KnowledgeScope RAG v0 (M5) | Agenter citerer kildefiler i svar | Svar inkluderer min. 1 citation; UI viser citation-chip der kan klikkes |
| Agent Chat Sidebar | Besked-panel med streaming tekst og citations | Delta-beskeder streamer tegn-for-tegn; auto-scroll til nyeste besked |
| Accessibility | Keyboard navigation + ARIA | Tab-navigation dækker hele MeetingRoom; screen reader kan læse agent-status |

### P2 — Ønskelig (v2+)

| Feature | Beskrivelse | Note |
|---------|-------------|------|
| LiveKit live media (M6) | Agent som lyd/video-deltager i LiveKit-rum | Afventer M3+M4; EU latency-krav kræver Scale-tier ($500/md) |
| Møde-opsummering (M7) | Beslutninger + action items auto-genereret | Afventer M5 (RAG nødvendig for kvalitetscitationer) |
| Model Lab / Compare (ADR-0006) | Blind side-by-side sammenligning af LLM-output | Implementeres i sidecar efter M2; Council før Compare |
| Teams + M365 (M8) | Join som Teams-bot, Entra-auth | Afventer Legal/Graph-permissions godkendelse |
| Voice cloning (M9) | Agent taler med specifik stemme | GDPR consent-flow krævet; consentStatus-felt allerede i datamodel |

---

## §5 Tech Stack

| Lag | Teknologi | Begrundelse |
|-----|-----------|-------------|
| Frontend | Next.js 15 (App Router) + React 19 + TypeScript | ADR-0001: Biyocon-basis; App Router for Server Components og streaming |
| Styling | Tailwind CSS v4 + shadcn/ui | Konsistent design-system; shadcn/ui giver tilgængelige komponenter out-of-box |
| Agent runtime | Python FastAPI (sidecar) | ADR-0005: Intelligens adskilt fra UI; Python-økoystem bedst til LLM/RAG |
| Video/audio | LiveKit Cloud EU | ADR-0003: WebRTC managed; EU-pinning; self-host exit via samme SDK |
| TTS | Azure Neural TTS (EU) | ADR-0004: M365-alignment; standard voices i MVP; EU-residency |
| STT | Whisper (Azure-hosted) | ADR-0004: Pair med TTS; Azure-hosted = EU-residency |
| Database | PostgreSQL + Chroma/pgvector | Relational for meetings/agents; vector for RAG |
| Auth | OAuth stub (MVP) → Entra ID (M8) | ADR-0002: Standalone-first; Teams-ready i arkitekturen |
| Package manager | pnpm | Monorepo-kompatibel; hurtigere end npm/yarn |

---

## §6 Successmetrikker

| Metrik | Målværdi | Deadline | Målemethod |
|--------|----------|----------|------------|
| M1 demo-møde klar | 1 talende agent-kort fungerer end-to-end | 2026-08-01 | Manuel demo-test med 4 mock-agenter |
| Agent-status latency | < 500ms fra `agent.status`-event til UI-opdatering | M1-milestone | Playwright test: event → DOM-ændring |
| TTS latency (M3) | < 1.5s fra LLM-svar til lyd i browser | 2026-09-15 | Automatisk benchmark via sidecar |
| STT latency (M4) | < 800ms fra tale-slut til transskription | 2026-09-15 | Automatisk benchmark |
| Disclosure compliance | 100% agent-kort viser disclosure-badge | M1-milestone | Visuelt review + E2E-test |
| RAG citation-rate (M5) | ≥ 80% af agent-svar inkluderer min. 1 citation | 2026-10-01 | Logging i sidecar |

---

## §7 Out of scope

- **Ikke i denne version (MVP):** Fotorealistiske avatarer, 3D-animationer, lip-sync
- **Ikke i denne version (MVP):** Direkte LLM-kald fra browser (alt via sidecar og contract)
- **Ikke i denne version (MVP):** Teams-møde-integration (M8+)
- **Ikke i denne version (MVP):** Voice cloning (M9+)
- **Ikke i denne version (MVP):** Rigtige brugerdata — kun testdata til MVP er lanceret
- **Ikke i denne version (MVP):** Mobiloptimering (tablet og desktop primary)
- **Muligvis fremtid (M8+):** AR/VR meeting room
- **Muligvis fremtid:** Agenters mulighed for at kalde externe APIs autonomt (human-approval i MVP)

---

## §8 Åbne spørgsmål

| Spørgsmål | Ansvarlig | Frist | Status |
|-----------|-----------|-------|--------|
| LiveKit Scale-tier ($500/md) — hvornår eskalerer vi fra Build-tier? | Produktejer | 2026-08-15 | ÅBEN |
| GDPR-legal-review for syntetisk stemme i EU-forretningskontekst | Legal + CISO | 2026-09-01 | ÅBEN |
| Azure Neural TTS: standard voices eller custom neural voice (CnV) til MVP? | ADR-0004 review | 2026-08-01 | ÅBEN |
| Model Lab (ADR-0006): Council eller Compare implementeres først? | ADR-0006 svar: Council | — | BESVARET |

---

## Ændringshistorik

| Dato | Version | Ændring | Årsag |
|------|---------|---------|-------|
| 2026-06-28 | 1.0 | Initial PRD udfyldt fra ADR-beslutninger | Tilpasning fra Cambuulo-template |
| 2026-06-28 | 1.1 | Tilføjet §6 metrikker med konkrete latency-krav | Acceptkriterie-præcisering |
| 2026-07-01 | 1.2 | Milestone-referencer realignet til stage-3-planen (M2 = sidecar-swap, ikke kun profile-loader); §5 uændret | Docs-drift-audit: KØREPLAN/DEPS var ude af sync med faktisk kode |
