---
status: accepted
---

# Python-sidecar til agent-runtime; TypeScript BFF i Biyocon

Vi skulle afgøre, hvor agent-runtimen (kerne-IP: RAG, egen/fælles brain, tool-policy, owner-scoping, multi-agent, audit) kører. **Beslutning:** agent-runtimen bygges som en **Python/FastAPI-sidecar** (inspireret af `odysseus`-mønstre); Biyocon/Next.js får en **tynd TypeScript BFF**, der ejer auth, room-state, LiveKit-token-flow, UI-events og streaming til frontend. **Princip: Biyocon ejer produktoplevelsen (kroppen); sidecar'en ejer intelligensen (hjernen).**

## Considered Options

- **(A) Python-sidecar + TS BFF** (valgt) — genbruger odysseus' sværest-vundne mønstre, rigeste agent/RAG/ML-økosystem, og en ren søm til self-host/lokale modeller senere. Koster to services/sprog.
- **(B) TS-native i Next.js** (fravalgt) — hurtigste MVP, ét stack, men svagere agent/RAG-økosystem og kan ikke genbruge odysseus' Python-mønstre → sandsynlig dyr omskrivning, når RAG/memory/multi-agent/lokale modeller modnes.

## Consequences

- **Kontrakt-først:** definér agent-event-kontrakten (WS/SSE/HTTP) op front, så runtimen er **udskiftelig** (samme portabilitetsprincip som ADR-0003/0004). Første demo må stubbe agent-svar i TS — men kun bag den endelige kontrakt.
- **Repo-roller afgjort:** `odysseus` = runtime-reference/komponent-donor; `custom` = agent/persona/skills-kilde; `iqra` = let reference (chat/session/transcribe).
- **Sidecar in-scope:** `AgentProfile`, `MeetingAgentInstance`, `KnowledgeScope`, `FileAccessGrant`, `ToolPermission`, `AuditEvent`, privat + fælles brain, RAG retrieval, tool dispatcher + policy, STT/TTS-orkestrering, event-streaming.
- **Biyocon/Next.js in-scope:** tabletop-UI, deltager-/agentpladser, LiveKit, UI-state (`idle/listening/thinking/speaking`), command palette/agent-controls, auth/session/BFF, WS/SSE mod sidecar, senere Teams-flader.
- **MVP out-of-scope:** fuld CrewAI/LangGraph-kompleksitet fra dag ét; self-hosted LLM som krav; avanceret multi-agent planning; fuld enterprise-file-connector-suite; autonom tool execution uden human approval.

## MVP minimal sidecar-overflade (v0)

`POST /agent/respond` · `GET /agent/events/{meetingId}` (SSE) · AgentProfile-loader fra `custom`-format · KnowledgeScope-stub · basal retrieval over én projektmappe/uploadet tekst · Azure TTS-adapter · Whisper STT-adapter/stub · audit-log pr. agent-handling.
