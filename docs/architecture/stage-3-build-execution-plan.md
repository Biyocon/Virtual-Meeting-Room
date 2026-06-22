# STAGE 3 — Build Execution Plan

> Omsætter Stage 2-kontrakten til en eksekverbar byggeplan. Forankret i Biyocons faktiske struktur
> (`app/`, `components/`, `hooks/`, `lib/{livekit,auth,privacy,offline}/`, `hooks/useMeetingRealtime`) og ADR-0001…0005.

---

## 1. Roadmap M0–M9

Pr. milepæl: **mål · leverancer · acceptkriterier · risici.**

**M0 — Kontrakt & skeleton**
- Mål: stabil Agent Event Contract + tomme skaller, så alt bygges bag kontrakten.
- Leverancer: TS-typer (`AgentEvent`, `AgentCommand`, `Meeting`, `MeetingAgentInstance`) i `lib/agent/contract.ts`; spejlet `sidecar/contracts.py`; BFF-endpoints; FastAPI-skelet; SSE-stub; audit-log-stub.
- Accept: en `agent.status`-event kan flyde UI ← BFF ← sidecar-stub via SSE.
- Risici: kontrakt-drift mellem TS/Python → afhjælpes med ét kildedokument + skema-test (afsnit 6).

**M1 — Tabletop agent card**
- Mål: ét talende digital-medarbejder-kort i rummet.
- Leverancer: `AgentCard`-komponent; status `idle→thinking→speaking→idle`; streaming-tekst fra stub; illustreret avatar-placeholder; **syntetisk-stemme-disclosure**.
- Accept: kortet skifter status og viser streamet tekst fra stubben; disclosure er synlig.
- Risici: status-flicker → debounce status-events.

**M2 — Sidecar v0**
- Mål: rigtig sidecar bag kontrakten.
- Leverancer: `POST /agent/respond`; `GET /agent/events/{meetingId}` (SSE); AgentProfile-loader fra `custom`-format; minimal `AuditEvent`; mock RAG/KnowledgeScope-stub.
- Accept: TS-stub udskiftes med sidecar **uden** UI-ændring (DoD, afsnit 4).
- Risici: SSE-forbindelsesstabilitet → heartbeat + reconnect.

**M3 — Azure TTS**
- Mål: agenten taler.
- Leverancer: Azure TTS-adapter (EU-region); `agent.audio`-event; client-side playback; retention/cache-regler.
- Accept: agent-svar afspilles som Azure-stemme; cache har sletteregel.
- Risici: residency → EU-ressource + ingen følsomme data (ADR-0003/0004).

**M4 — Whisper/STT-stub**
- Mål: kontekst fra tale/transskript.
- Leverancer: uploadet/simuleret transcript → sidecar-kontekst; audit på transcript-brug.
- Accept: transcript påvirker agent-svaret; brug logges.
- Risici: PII i transcript → testdata-only.

**M5 — KnowledgeScope v0 (RAG)**
- Mål: agent svarer ud fra projektdata.
- Leverancer: én uploadet tekstfil/projektmappe; basal retrieval; **citations** i `agent.message.final`.
- Accept: svar indeholder citation til kilden i KnowledgeScope.
- Risici: RAG-hallucination → citation-krav + "ved ikke"-fallback.

**M6 — LiveKit live**
- Mål: ægte media + agent som deltager.
- Leverancer: rigtige menneske-tracks; agent publicerer audio som LiveKit-track (forudsætning for Teams media-bot senere).
- Accept: menneske + agent-audio i samme room.
- Risici: WebLatency/track-publish → fald tilbage til client-side playback.

**M7 — Meeting intelligence**
- Mål: output fra mødet.
- Leverancer: `meeting.summary`, beslutningslog, action items.
- Accept: opsummering + beslutninger/actions kan eksporteres.

**M8 — Teams-ready + M365 (fase 2)**
- Mål: Teams-sidepanel + scoped filadgang.
- Leverancer: Entra ID-auth mappet til `lib/auth`; Teams sidepanel/meeting-tab mod samme BFF; scoped Graph/OneDrive/SharePoint-connectors via `FileAccessGrant`.
- Accept: agent kan tilgå én SharePoint/OneDrive-kilde under et Teams-møde, auditeret.
- Risici: Graph scopes/permissions → mindst-privilegium, admin-consent.

**M9 — Enterprise & self-host exit**
- Mål: governance + portabilitet indfries.
- Leverancer: self-host LiveKit + Azure-container/odysseus-TTS; tenant-isolation; admin/audit-dashboard; voice cloning (egen samtykke-gated ADR); avancerede avatarer.
- Accept: samme app kører self-hosted i EU/DK uden frontend-omskrivning.

## 2. Risikoanalyse

| Risiko | Sandsynl. | Effekt | Afbødning |
|---|---|---|---|
| Teams permissions/Graph scopes | Høj | Høj | Fase 2+; mindst-privilegium; admin-consent; udskyd media-bot |
| WebRTC latency | Mellem | Mellem | LiveKit Cloud EU; client-side TTS-fallback i MVP |
| Media-bot complexity | Høj | Høj | Fase 4; genbrug LiveKit-track-model fra M6 |
| Prompt injection (dokumentkilder) | Høj | Høj | Sanitér RAG-input; system-prompt-isolation; tool-policy |
| File access leakage | Mellem | Høj | `FileAccessGrant` + owner-scoping + audit pr. adgang |
| RAG-hallucination | Høj | Mellem | Citation-krav; "ved ikke"-fallback; retrieval-confidence |
| Voice cloning consent | Mellem | Høj | Udskudt; samtykke-gated ADR; Azure Custom/Personal Voice-flow |
| GDPR/residency | Høj | Høj | Testdata-only MVP; EU-endpoints; observability fra; self-host-exit |
| Multi-tenant isolation | Mellem | Høj | `tenantId` på alt; scoping fra dag ét |
| Provider lock-in | Mellem | Mellem | Adapter-baseret media/voice/LLM (ADR-0003/0004/0005) |
| Cost (LiveKit Scale-tier/TTS) | Mellem | Mellem | Build/Ship-tier + testdata i MVP; mål omkostning før Scale |
| Browser limitations | Lav | Mellem | LiveKit SDK håndterer; test på mål-browsere |
| Avatar complexity | Lav | Lav | 2D speaking-state i MVP (style spec) |
| Kontrakt-drift TS/Python | Mellem | Mellem | Ét kontrakt-kildedokument + skema-test |

## 3. Første 10 implementeringsopgaver

1. Definér `AgentEvent` + `AgentCommand` (envelope + typer) i `lib/agent/contract.ts`.
2. Spejl kontrakten i `sidecar/contracts.py` + skema-test der fejler ved drift.
3. BFF: `app/api/agent/respond/route.ts` (command-proxy → sidecar).
4. BFF: `app/api/agent/events/[meetingId]/route.ts` (SSE-stream UI ← sidecar).
5. FastAPI-skelet: `sidecar/app.py` + tom `POST /agent/respond` + `GET /agent/events/{meetingId}`.
6. `hooks/useAgentEvents.ts` (SSE-client) + integrér i `hooks/useMeetingRealtime`.
7. `components/agent-card.tsx`: status (idle/thinking/speaking), illustreret avatar-placeholder, waveform/ring, syntetisk-stemme-disclosure.
8. Sidecar: `AgentProfile`-loader fra `custom`-frontmatter (`profile.md` + `skills.yaml`).
9. Sidecar: `audit.py` — emit `AuditEvent` ved hver agent-handling.
10. End-to-end stub: `agent.respond` → streamede `agent.message.delta` → `agent.message.final`, vist i kortet.

## 4. Definition of Done — MVP Agent Sidecar v0

- `POST /agent/respond` accepterer `{meetingId, agentInstanceId, prompt, knowledgeScopeId}` og streamer `agent.message.delta` → `agent.message.final` over `GET /agent/events/{meetingId}` (SSE).
- AgentProfile loades fra `custom`-format (`id/name/role/avatar/accent/skills/systemPrompt`).
- Hver agent-handling emitter et `AuditEvent` (actor, action, ts).
- KnowledgeScope er en stub, men kontrakten (`sources[]`, citations-felt) er på plads.
- TS-stubben fra M1 kan udskiftes med sidecar'en **uden ændring i UI eller kontrakt**.
- Owner-scoping (`tenantId`, `meetingId`, `agentInstanceId`) håndhæves på alle kald.
- Kun testdata; ingen følsomme kilder.

## 5. Repo-ændringsplan

**Biyocon (udvid eksisterende struktur — greenfield kun for agent-laget):**
```
app/api/agent/respond/route.ts            (ny) command-proxy → sidecar
app/api/agent/events/[meetingId]/route.ts (ny) SSE-stream ← sidecar
lib/agent/contract.ts                     (ny) AgentEvent/AgentCommand/Meeting/MeetingAgentInstance
lib/agent/sidecarClient.ts                (ny) HTTP/SSE-klient mod sidecar
lib/livekit/*                             (genbrug) token/room
lib/auth/*                                (genbrug; Teams-ready senere)
lib/privacy/*                             (genbrug; disclosure/retention-hooks)
hooks/useAgentEvents.ts                   (ny) SSE-client
hooks/useMeetingRealtime.ts               (udvid) integrér agent-events
components/agent-card.tsx                  (ny) tabletop-plads m. status + disclosure
components/tabletop/*                      (udvid) placér agent-kort ved bordet
```

**Sidecar (ny Python/FastAPI-tjeneste):**
```
sidecar/app.py                 FastAPI-app
sidecar/routes/agent.py        POST /agent/respond, GET /agent/events/{meetingId}
sidecar/contracts.py           spejl af AgentEvent/AgentCommand (skema-testet mod TS)
sidecar/runtime/profile_loader.py   AgentProfile fra custom-format
sidecar/runtime/instance.py    MeetingAgentInstance-lifecycle + owner-scoping
sidecar/runtime/brain.py       privat/fælles brain (stub→memory)
sidecar/runtime/rag.py         KnowledgeScope retrieval (stub→Chroma/pgvector)
sidecar/policy.py              ToolPermission/policy-checks (human-in-the-loop)
sidecar/audit.py               AuditEvent
sidecar/adapters/tts_azure.py  Azure Neural TTS (EU)
sidecar/adapters/stt_whisper.py Whisper
sidecar/adapters/llm.py        OpenAI/Anthropic/Ollama
```

## 6. Testplan — Agent Event Contract (BFF ↔ sidecar ↔ UI)

- **Kontrakttest:** valider `AgentEvent`/`AgentCommand` mod ét delt JSON-skema fra både TS- og Python-side; CI fejler ved drift (afbøder kontrakt-drift-risikoen).
- **Integrationstest (BFF↔sidecar):** `agent.respond` → forvent ordnet `agent.status: thinking` → ≥1 `agent.message.delta` → `agent.message.final` på SSE-streamen.
- **UI-test:** givet en sekvens af events rendrer `AgentCard` korrekt `idle→thinking→speaking→idle` og akkumulerer delta-tekst til final.
- **Audit-assertion:** hver `agent.respond` producerer mindst ét `AuditEvent` med korrekt `actor`/`meetingId`.
- **Scoping-test:** kald med forkert `tenantId`/`meetingId` afvises.
- **Streaming-robusthed:** SSE-reconnect midt i en stream genoptager uden dublet-final.

## 7. Første Claude Code / Codex-kodeprompt (M0–M1)

> Kopiér ind i Claude Code/Codex i Biyocon-repoet, med `STAGE-2-architecture.md` + ADR'erne tilgængelige.

```text
KONTEKST: Du arbejder i Biyocon-Virtual-Meeting-Room (Next.js 15/React 19/Tailwind/shadcn).
Arkitektur og kontrakt er låst i STAGE-2-architecture.md og ADR-0001…0005. Genåbn dem ikke.
Princip: Biyocon ejer UI/BFF; en separat Python-sidecar ejer intelligensen. Byg ALT bag den
stabile Agent Event Contract, så en TS-stub senere kan udskiftes med sidecar uden UI-ændring.

OPGAVE (M0 + M1):
1. Opret lib/agent/contract.ts med TypeScript-typerne AgentEvent, AgentCommand, Meeting og
   MeetingAgentInstance præcis som i STAGE-2-architecture.md (envelope: type/meetingId/
   agentInstanceId?/ts/correlationId/payload).
2. Opret BFF-endpoints:
   - app/api/agent/respond/route.ts: modtager en AgentCommand, kalder (foreløbig) en lokal
     TS-stub, returnerer 202.
   - app/api/agent/events/[meetingId]/route.ts: SSE-endpoint der streamer AgentEvents.
3. Lav en TS-stub (lib/agent/stub.ts) der ved 'agent.respond' emitter: agent.status:thinking →
   3–5 agent.message.delta (streaming-tekst) → agent.message.final → agent.status:idle.
4. Opret hooks/useAgentEvents.ts (EventSource-client) og integrér i hooks/useMeetingRealtime.
5. Opret components/agent-card.tsx: en tabletop-plads med illustreret avatar-placeholder,
   status-badge (idle/listening/thinking/speaking), aktiv-taler-ring, waveform, rolle-label og
   en tydelig 'syntetisk stemme'-disclosure. Akkumulér delta-tekst til final.
6. Tilføj en audit-stub (lib/agent/audit.ts) der logger hver agent-handling lokalt.

KRAV:
- Ingen browser-storage (localStorage/sessionStorage).
- Owner-scoping (tenantId/meetingId/agentInstanceId) skal være i alle typer og kald.
- Kun testdata. Ingen rigtige model-/TTS-kald endnu (det er M2/M3).
- Skriv en kort kontrakttest der validerer AgentEvent/AgentCommand mod et JSON-skema.

DEFINITION OF DONE: Et agent-kort i rummet skifter idle→thinking→speaking→idle og viser
streamet stub-tekst via SSE, med disclosure synlig og audit-log pr. handling.
```
