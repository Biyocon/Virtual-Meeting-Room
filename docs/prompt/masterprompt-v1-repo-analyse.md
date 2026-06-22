# MASTERPROMPT — Analyse, repo-vurdering og produktarkitektur for "AI Virtual Meeting Room med digitale medarbejdere"

> Konverteret fra `AI Virtual Meeting Room Analysis.pdf`. Kanonisk masterprompt (afløser den tidligere kompakte `repo-analyse.md`).

Du er **senior softwarearkitekt, AI-product lead, WebRTC-specialist, Microsoft Teams-app-arkitekt og principal frontend engineer**.

Din opgave er at gennemgå de vedhæftede filer, repo-pakker og arkitekturdokumenter grundigt og systematisk for at afklare, hvilke GitHub-repositories og kodebaser jeg kan bruge som:

1. direkte fundament,
2. teknisk reference,
3. inspirationskilde,
4. komponentkilde,
5. eller noget der bør fravælges.

Projektet er en "AI Virtual Meeting Room"-platform, hvor menneskelige deltagere og digitale medarbejdere kan deltage i samme møde. Produktet skal på sigt kunne fungere som en app/plugin til Microsoft Teams, hvor man kan invitere eller tilføje digitale medarbejdere direkte i et igangværende Teams-møde.

## 1. Produktvision

Jeg vil bygge et virtuelt møderum, der funktionelt minder om Teams, men visuelt har et mere avanceret og produktorienteret UI.

Kerneideen er et virtuelt mødelokale set oppefra, hvor deltagerne sidder rundt om et skrivebord eller mødebord. På skærmen skal man kunne se både menneskelige mødedeltagere og digitale medarbejdere/AI-agenter. De digitale medarbejdere skal vises visuelt med avatar, rolle, status, stemmeindikator og eventuelt aktiv-taler-animation.

Møderummet skal kunne indeholde:

- menneskelige deltagere,
- digitale medarbejdere,
- delt skærm,
- fælles dokumenter,
- projektmapper,
- chat,
- live-transskription,
- beslutningslog,
- action items,
- mødeopsummering,
- agent-svar baseret på projektets data,
- og senere dybere integration til Microsoft 365, SharePoint, OneDrive, Google Drive, Dropbox og andre filkilder.

## 2. Digitale medarbejdere

Digitale medarbejdere skal kunne oprettes med:

- navn,
- persona,
- avatar,
- rolle,
- fagområde,
- særskilt stemme,
- eventuel stemmekloning,
- standardsprog,
- skills,
- system prompt,
- privat "brain",
- fælles projekt-brain,
- adgang til videnbase,
- adgang til projektmappe,
- adgang til udvalgte filer,
- auditérbare handlinger,
- rettighedsniveau,
- og meeting behavior-regler.

De skal kunne tale og svare som ChatGPT, men fremstå visuelt som deltagere i mødet. De skal kunne deltage i mødet på basis af deres rolle, eksempelvis som projektleder, data engineer, udbudskonsulent, juridisk rådgiver, teknisk granskende agent, referent eller mødefacilitator.

## 3. Vedhæftede repo- og filkontekster

Du skal gennemgå og verificere indholdet i de vedhæftede filer. Du må ikke blindt antage, at denne beskrivelse er korrekt. Brug den som foreløbig hypotese og bekræft eller korrigér den ud fra kildefilerne.

De vigtigste input er:

### A. Biyocon-Virtual-Meeting-Room

Foreløbig hypotese:

- Next.js / React / Tailwind / shadcn/ui.
- Eksisterende møderums-UI.
- Deltagerkort, avatarer, aktiv taler, skærmdeling, dokument-upload, controls.
- Indikationer på ønsket LiveKit/WebRTC-arkitektur.
- Mulig tabletop/desk-vision i PRD/masterprompt.

**Analyseopgave:** Vurder om dette repo bør være primær produktbase for UI/MVP. Kortlæg komponentstruktur, teknisk modenhed, mangler, styrker, integrationspunkter og refaktorbehov.

### B. custom

Foreløbig hypotese:

- Indeholder digitale medarbejdere/personaer.
- Agent-profiler med `profile.md`.
- Skills pr. agent via `skills.yaml`.
- Avatar-assets.
- Agent registry.
- Agent brain, memory, decisions, maps og runbooks.
- Mulige spor af Teams, CrewAI, LangGraph eller multi-agent-runtime.

**Analyseopgave:** Vurder om dette repo bør være fundament for agent-kataloget, persona-definitioner, skills, rollebeskrivelser og "digital employee"-konceptet. Identificér hvilken agent-model der bør standardiseres.

### C. odysseus

Foreløbig hypotese:

- Python/FastAPI-baseret self-hosted AI-platform.
- Local-first AI workspace.
- Ollama/local model serving.
- STT/TTS.
- Memory.
- RAG/ChromaDB.
- Search/SearXNG.
- Scheduler.
- Tool execution.
- Security boundaries.
- Upload/document handling.
- Mulig arkitektur for AI-runtime, "brain", knowledge og tool-dispatcher.

**Analyseopgave:** Vurder om Odysseus bør bruges som backend/AI-runtime-reference. Identificér hvilke dele der bør klones som domænekontrakter og hvilke dele der ikke bør klones direkte. Vurder især RAG, memory, skills, STT/TTS, SSE-streaming, tool-policy og owner-scoping.

### D. iqra

Foreløbig hypotese:

- Node/TypeScript API-server.
- Express.
- OpenAI integration.
- Chat, sessions, transcribe.
- React/shadcn mockup.
- Mulig lettere samtale-/transskriptionsarkitektur.

**Analyseopgave:** Vurder om Iqra kan bruges som let TypeScript-baseret samtale- og session-layer, eller om det kun bør bruges som inspirationskilde. Sammenlign med Odysseus og Biyocon Virtual Meeting Room.

### E. MiroTalk SFU

Foreløbig hypotese:

- Modent WebRTC/SFU-projekt.
- Mediasoup-baseret video.
- Room management.
- API'er til join/meeting/token.
- Recording/RTMP.
- Auth/JWT/OIDC.
- ChatGPT/DeepSeek integration.
- LiveAvatar/video AI-konfiguration.
- Transcription/UI flags.

**Analyseopgave:** Vurder om MiroTalk SFU kan bruges som direkte basis, referencearkitektur eller kun som inspiration. Sammenlign med LiveKit-sporet. Vurder trade-offs mellem:

- bygge oven på MiroTalk SFU,
- bruge LiveKit i egen Next.js-app,
- bruge MiroTalk SFU som separat service,
- eller kun genbruge mønstre/API-design.

### F. VSCodium

Foreløbig hypotese:

- Ikke relevant som meeting-room-produktbase.
- Kan være relevant som inspiration til distribution, patching, open-source build workflows, multi-platform packaging og CI/CD.

**Analyseopgave:** Vurder om VSCodium overhovedet er relevant for dette projekt. Hvis ja, afgræns præcist hvordan. Undgå at overdrive relevansen.

### G. Odysseus architecture map / Excalidraw

Foreløbig hypotese:

- Indeholder arkitekturkort over FastAPI, raw ESM frontend, local-first AI workspace, Chroma, SearXNG, memory, tools, policy, scheduler, model ops og runtime flows.

**Analyseopgave:** Udtræk arkitektoniske principper, der kan omsættes til AI Virtual Meeting Room: agent runtime, memory/RAG, tool-policy, session isolation, owner-scoping, background jobs, audit og SSE-streaming.

## 4. Primære spørgsmål der skal besvares

Besvar følgende spørgsmål grundigt:

1. Hvilket repo bør være primær base for MVP?
2. Hvilke repos bør kun bruges som inspirationskilde?
3. Hvilke repos bør bruges som reference for specifikke delsystemer?
4. Bør jeg bygge videre på MiroTalk SFU eller bruge LiveKit i mit eget produkt?
5. Hvordan bør jeg integrere digitale medarbejdere i møderummet?
6. Hvordan bør agent/persona/skill/brain-modellen se ud?
7. Hvordan bør Teams-integrationen fases?
8. Hvordan bør Microsoft 365, SharePoint, OneDrive, Google Drive og Dropbox-adgang designes?
9. Hvordan bør voice, STT, TTS og voice cloning fases?
10. Hvordan bør avatar-niveauet fases: statisk 2D, speaking-state, lip-sync, 3D?
11. Hvilke GDPR-, sikkerheds- og compliancekrav skal tænkes ind fra starten?
12. Hvilken teknisk roadmap bør jeg følge fra demo-MVP til enterprise-version?

## 5. Beslutningsantagelser

Brug følgende som anbefalede beslutningsrammer, medmindre kildefilerne viser noget andet:

### Teams target surface

Start med Teams in-meeting app, sidepanel og meeting tab som MVP. Design til senere real-time media-bot, men byg ikke media-bot først.

**Forklaring:** En Teams in-meeting app er hurtigere at få til MVP, lettere at godkende og bedre egnet til UI, agentkontrol, chat, dokumentvalg og mødeopsummering. Real-time media-bot bør være fase 2 eller 3.

### Hosting og runtime

Brug hybrid arkitektur.

**Primær produktstack:**

- TypeScript
- Next.js
- React
- Tailwind
- shadcn/ui
- Microsoft Teams app SDK
- Microsoft Graph
- LiveKit eller tilsvarende WebRTC/SFU-lag

**AI-service-lag:**

- Python/FastAPI eller Node service afhængigt af funktion
- RAG/vector DB
- STT/TTS
- agent runtime
- tool dispatcher
- file connectors
- memory service
- audit log

Cloud-API'er må bruges til hurtig MVP, men arkitekturen skal kunne udskifte dem med self-hosted/Odysseus-lignende services.

### Skala

**MVP:**

- ét aktivt møde ad gangen,
- 3–8 menneskelige deltagere,
- 1–3 digitale medarbejdere,
- én projektmappe/videnbase pr. møde.

**Senere:**

- multi-tenant,
- flere samtidige møder,
- mange agenter,
- rollebaseret adgang,
- enterprise audit og governance.

### Compliance

Antag GDPR som standardkrav. Inkludér:

- Entra ID/OAuth,
- least privilege,
- dataminimering,
- audit logs,
- samtykke til optagelse/transskription,
- samtykke til voice cloning,
- tydelig markering af syntetiske stemmer,
- adgangslog for filer,
- tenant isolation,
- sletning/retention,
- kryptering,
- prompt-injection-beskyttelse for dokumentkilder,
- og ingen ukontrolleret adgang til brugerens filer.

### Avatar og voice

**Start med:**

- 2D avatar,
- aktiv-taler-ring,
- waveform,
- speaking-state,
- status-badges,
- rollelabel,
- model/agentlabel.

**Udskyd:**

- lip-sync,
- 3D-avatar,
- real-time facial animation,
- avanceret voice cloning.

Voice cloning skal behandles som reguleret feature med eksplicit consent-flow.

## 6. Analysemetode

Arbejd systematisk i følgende rækkefølge:

### Trin 1 — Repo-inventar

For hvert repo/filpakke: identificér stack, frameworks, runtime, build system, API'er, integrationspunkter, UI-komponenter, datamodeller, sikkerhedsmekanismer, modenhed, testdækning, dokumentation, og kendte risici.

### Trin 2 — Domænemapping

Map hvert repo til disse domæner:

- Meeting UI
- WebRTC/SFU
- Teams integration
- Agent/persona registry
- Skills
- Brain/memory
- RAG/knowledge base
- STT
- TTS
- Voice cloning
- Avatar rendering
- File connectors
- Microsoft 365/Graph
- Dropbox/Google Drive/OneDrive/SharePoint
- Session management
- Audit/compliance
- CI/CD/distribution

### Trin 3 — Fit-score

Lav en vægtet score fra 1–5 for hvert repo på: produktfit, teknisk modenhed, kodekvalitet, integrationsværdi, genbrugsgrad, kompleksitet, sikkerhedsrisiko, MVP-hastighed, enterprise-egnethed, og lock-in risiko. Forklar hver score kort og konkret.

### Trin 4 — Arkitekturbeslutning

Giv en klar anbefaling:

- "Byg oven på X"
- "Brug Y som reference"
- "Udtræk Z som modul"
- "Fravælg A som base"
- "Brug B kun til inspiration"

Undgå vage formuleringer. Giv en prioriteret beslutning.

### Trin 5 — MVP-arkitektur

Design en MVP-arkitektur med: frontend, meeting room UI, participant model, digital employee model, agent runtime, LiveKit/WebRTC eller MiroTalk decision, session store, file access, RAG, STT/transcription, TTS, meeting summary, audit log, Teams sidepanel, og Graph/OAuth integration.

### Trin 6 — Enterprise-arkitektur

Design en senere enterprise-arkitektur med: multi-tenant, Entra ID, Microsoft Graph, SharePoint/OneDrive, Google Drive/Dropbox connectors, scoped file grants, RAG indexing pipeline, consent management, voice governance, audit trail, admin dashboard, agent marketplace/catalog, policy engine, og deployment model.

## 7. Outputformat

Lever svaret i denne struktur:

### 1. Executive summary

Kort konklusion: bedste primærbase, bedste WebRTC-strategi, bedste agent-strategi, bedste Teams-strategi, vigtigste risici.

### 2. Repo-by-repo analyse

For hvert repo: formål, teknisk stack, relevante moduler, hvad kan genbruges, hvad bør ikke genbruges, risici, anbefalet rolle i projektet.

### 3. Sammenligningsmatrix

Lav tabel med: repo, egnethed som base, egnethed som reference, domæne, score, anbefaling.

### 4. Beslutning: Hvad skal jeg bygge oven på?

Giv en tydelig anbefaling: primær base, sekundære inspirationskilder, komponenter der bør udtrækkes, komponenter der bør bygges fra bunden.

### 5. MiroTalk SFU vs LiveKit

Lav særskilt analyse: fordele ved MiroTalk SFU, ulemper ved MiroTalk SFU, fordele ved LiveKit, ulemper ved LiveKit, anbefalet valg for MVP, anbefalet valg for enterprise.

### 6. Teams-integrationsstrategi

Foreslå faser:

- **Fase 1:** Teams sidepanel / meeting tab / in-meeting app.
- **Fase 2:** Meeting context, Graph, mødeopsummering, participant mapping, filvalg.
- **Fase 3:** Real-time media-bot eller dybere mødeintegration.
- **Fase 4:** Enterprise governance, admin policies, tenant-wide deployment.

### 7. Digital employee model

Definér en konkret datamodel for: `AgentProfile`, `AgentPersona`, `AgentVoice`, `AgentAvatar`, `AgentSkill`, `AgentBrain`, `MeetingAgentInstance`, `KnowledgeScope`, `FileAccessGrant`, `ToolPermission`, `AuditEvent`. Inkludér felter, relationer og principper.

### 8. Brugerflows

Beskriv trin-for-trin: opret møde, tilføj menneskelige deltagere, tilføj digital medarbejder, vælg agentrolle, vælg projektmappe, giv filadgang, start møde, agent lytter/læser kontekst, agent svarer, agent genererer actions, mødet afsluttes, opsummering eksporteres.

### 9. UI/UX-koncept

Beskriv tabletop meeting room: top-down desk layout, central stage, delt skærm/dokument, deltagere rundt om bordet, digitale medarbejdere visuelt adskilt men ikke isoleret, active speaker states, agent status states, controls, sidepanel, chat, transcript, agent command palette. Inkludér low-fidelity wireframes i ASCII.

### 10. Arkitekturdiagrammer

Inkludér tekstbaserede diagrammer for: MVP systemarkitektur, Teams app arkitektur, agent runtime, file/RAG pipeline, meeting event flow, voice/STT/TTS pipeline, security/compliance boundary.

### 11. Roadmap

Lav roadmap:

- **M0** — Analyse og beslutning
- **M1** — UI prototype
- **M2** — LiveKit/WebRTC MVP
- **M3** — Agent catalog
- **M4** — RAG/project knowledge
- **M5** — Teams in-meeting app
- **M6** — STT/TTS
- **M7** — Meeting intelligence
- **M8** — Enterprise governance
- **M9** — Advanced avatars/voice cloning

For hver milepæl: mål, leverancer, tekniske opgaver, acceptkriterier, risici.

### 12. Risikoanalyse

Dæk mindst: Teams permissions, Microsoft Graph scopes, WebRTC latency, media-bot complexity, prompt injection, file access leakage, RAG hallucination, voice cloning consent, GDPR, multi-tenant isolation, model/provider lock-in, cost, scaling, browser limitations, avatar/lip-sync complexity.

### 13. Endelig anbefaling

Afslut med: præcis anbefalet stack, anbefalet repo-strategi, første 10 konkrete implementeringsopgaver, og hvilke beslutninger der bør låses nu versus senere.

## 8. Arbejdsregler

- Opfind ikke konkret kodeadfærd uden evidens.
- Markér antagelser eksplicit.
- Skeln mellem "fundet i repo", "inferred", og "anbefaling".
- Vær konkret.
- Prioritér MVP-hastighed, men design uden at blokere enterprise-version.
- Vær kritisk: fravælg repos/moduler hvis de ikke passer.
- Brug ikke generiske anbefalinger uden at koble dem til repo-indholdet.
- Giv klare beslutninger, ikke kun muligheder.
