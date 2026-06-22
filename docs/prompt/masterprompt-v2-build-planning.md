# MASTERPROMPT v2.0 — AI Virtual Meeting Room (beslutningslåst build-planning-prompt)

> Kopiér hele blokken ind i Claude Code / Codex / Claude / ChatGPT **sammen med de fire repomix-filer**
> (`repomix-output-Biyocon-Virtual-Meeting-Room.txt`, `repomix-custom-output.md`,
> `repomix-odysseus-output.md`, `Iqra.md`/`repomix-iqra-output.md`, `mirotalksfu.md` som reference)
> og `odysseus-architecture-map.excalidraw`.

---

## 0. Sådan bruges denne prompt

Arkitekturbeslutningerne er **LÅST** (ADR-0001…0005, afsnit 3). Denne prompt **genåbner ikke** repo-valg, base, media-, voice- eller runtime-beslutninger. Den driver **Stage 2** (arkitektur + datamodel + flows) og **Stage 3** (roadmap + risici + backlog + første kode-fase), givet de vedlagte filer som reference. Hvis du finder en stærk grund til at udfordre en låst beslutning, så **genåbn den ikke** — flag den separat som forslag til en ny ADR.

## 1. Rolle

Du er senior softwarearkitekt, AI-product lead, WebRTC/LiveKit-specialist, Microsoft Teams/M365-app-arkitekt og principal frontend engineer. Du arbejder evidensbaseret og skelner eksplicit mellem **"fundet i repo"**, **"inferred"** og **"anbefaling"**.

## 2. Produktvision + UX-retning (eksplicit)

Et virtuelt **tabletop-mødelokale set oppefra**, hvor **menneskelige deltagere og digitale medarbejdere** sidder rundt om samme bord. Digitale medarbejdere vises som pladser med **avatar + rolle + status + stemmeindikator + aktiv-taler-state**. Rummet har fælles projektmappe/videnscope og fælles "brain". Man kan tale med en digital medarbejder som med ChatGPT, men agenten fremstår visuelt som en deltager. Teams-sidepanel/meeting-tab kommer først; media-bot senere.

## 3. Låste beslutninger (constraints — må ikke genåbnes)

| Emne | Beslutning | Kilde |
|---|---|---|
| Primær base | **Biyocon** (Next.js 15/React 19/Tailwind/shadcn) | ADR-0001 |
| Media-strategi | **Standalone tabletop-rum med egen real-time media**; Teams = senere kanal (faset) | ADR-0002 |
| Media-transport | **LiveKit** (Apache-2.0); MiroTalk SFU = WebRTC/SFU-**reference** (AGPLv3/kommerciel — ikke base) | ADR-0002/0003 |
| Media-deployment | **LiveKit Cloud, kun testdata** i MVP → **self-host som enterprise-exit**; deployment-portabelt | ADR-0003 |
| Voice (TTS) | **Azure Neural TTS (EU-region)** standardstemmer; ElevenLabs/self-host senere; **voice cloning udskudt** (samtykke-gated) | ADR-0004 |
| Voice (STT) | **Whisper** | ADR-0004 |
| Avatar | **Illustreret 2D portræt + speaking-state**; ingen lip-sync/3D i MVP | avatar style spec |
| Agent-runtime | **Python/FastAPI-sidecar** (odysseus-mønstret) + **tynd TS BFF** i Biyocon; kontrakt-først, runtime udskiftelig | ADR-0005 |
| Repo-roller | Biyocon=base · `custom`=persona/skills-kilde · `odysseus`=runtime-reference/donor · `iqra`=let reference · MiroTalk=SFU-reference · VSCodium=ude af scope | ADR-0001/0005 |

**Princip på tværs:** Biyocon ejer produktoplevelsen (kroppen); Python-sidecar'en ejer intelligensen (hjernen). Alt media/voice/runtime bygges adapter-/kontraktbaseret, så Cloud→self-host kan skiftes uden frontend-omskrivning.

## 4. Inputmateriale (reference — verificér ved gennemlæsning)

- **Biyocon** — tabletop møde-UI + LiveKit-wiring (base).
- **`custom`** — agent-katalog: `profile.md` + `skills.yaml` + `Avatar/` + registry + brain (persona/skills-kilde).
- **`odysseus`** — Python/FastAPI; RAG (Chroma), memory, STT/TTS, tool-policy, owner-scoping, scheduler (runtime-reference/donor; klon ikke wholesale — indeholder AGPL-dele).
- **`iqra`** — Node/TS Express + OpenAI + Whisper + `ws`; chat/session/transcribe (let reference).
- **MiroTalk SFU** — mediasoup/socket.io/express/JWT/Swagger/RTMP (WebRTC/SFU-reference; **AGPLv3/kommerciel** — kun mønstre/API-design, ikke kode-base).
- **odysseus-arkitekturkort** — principper for agent-runtime/RAG/owner-scoping.

## 5. Compliance (førsteordenskrav — verificeret)

- **LiveKit residency:** region pinning kun på Scale-tier ($500/md), skal anmodes via Support, **slår failover fra**; **observability-data lagres i USA** → slå fra ved residency-krav; **model-API'er routes uafhængigt** → brug EU-endpoints. MVP = kun testdata.
- **Azure Speech residency:** data forbliver i ressourcens region (vælg EU); container/edge-exit muligt; Custom/Personal Voice har **indbygget samtykke-/godkendelsesflow** (brug det til den senere kloning-ADR).
- **Tværgående:** syntetisk-stemme-disclosure i UI; retention for TTS-logs/audio/transskript; **owner-scoping** (`meetingId/tenantId/agentInstanceId/knowledgeScopeId/fileAccessGrantId`); prompt-injection-beskyttelse for dokumentkilder; least privilege; ingen ukontrolleret filadgang.

## 6. Staged output (det du skal levere)

### STAGE 2 — Arkitektur + datamodel + flows
1. **Mål-arkitektur:** Biyocon (TS BFF) + Python agent-sidecar + LiveKit + Azure TTS + Whisper + RAG + DB. Komponenter, ansvar, og **agent-event-kontrakten** (WS/SSE/HTTP) som tekstdiagram.
2. **Datamodel** (felter, relationer, owner-scoping): `AgentProfile`, `AgentPersona`, `AgentVoiceProfile` (jf. ADR-0004: `voiceProvider/voiceId/language/style/speakingRate/pitch/consentStatus/syntheticVoiceDisclosure`), `AgentAvatar`, `AgentSkill`, `AgentBrain` (privat + fælles), `MeetingAgentInstance`, `KnowledgeScope`, `FileAccessGrant`, `ToolPermission`, `AuditEvent`.
3. **Dataflows** (trin-for-trin): opret møde → tilføj menneskelige deltagere → tilføj digital medarbejder → vælg rolle → vælg projektmappe/videnscope → giv filadgang → start → agent lytter/læser kontekst (RAG) → svarer (tekst → TTS) → genererer actions → mødet afsluttes → opsummering eksporteres. Plus voice/STT/TTS-pipeline og fremtidig Teams-integrationsflade.

### STAGE 3 — Roadmap + risici + backlog + første kode-fase
4. **Roadmap M0–M9** med **MVP Agent Sidecar v0** (`POST /agent/respond`, `GET /agent/events/{meetingId}` SSE, AgentProfile-loader fra `custom`-format, KnowledgeScope-stub, basal retrieval, Azure TTS-adapter, Whisper-adapter/stub, audit-log) som tidligt mål. Pr. milepæl: mål, leverancer, opgaver, acceptkriterier, risici.
5. **Risikoanalyse** (mindst): Teams permissions, Graph scopes, WebRTC latency, media-bot complexity, prompt injection, file access leakage, RAG hallucination, voice cloning consent, GDPR, multi-tenant isolation, provider lock-in, cost, scaling, browser limitations, avatar complexity.
6. **Implementeringsbacklog:** de første 10 konkrete opgaver.
7. **Første kode-fase-prompt** til Claude Code/Codex: scaffold Biyocon TS BFF + agent-event-kontrakt + Python sidecar v0 + ét talende agent-kort i tabletop-rummet (statisk illustreret avatar + speaking-state + Azure TTS), med audit-log og owner-scoping fra start.

## 7. Arbejdsregler

- Skeln eksplicit "fundet i repo" / "inferred" / "anbefaling".
- **Genåbn ikke** låste beslutninger (afsnit 3); udfordringer flagges som forslag til ny ADR.
- Konkret og MVP-hurtigt, men design uden at blokere enterprise-fasen.
- Hold MVP-data-scope: kun testdata, ingen følsomme kilder/optagelser før compliance er lukket.
- Marker antagelser; vær kritisk; giv klare beslutninger, ikke kun muligheder.
