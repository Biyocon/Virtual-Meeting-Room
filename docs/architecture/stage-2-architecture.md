# STAGE 2 — Mål-arkitektur, datamodel & flows

> Den tekniske kontrakt for AI Virtual Meeting Room, forankret i de fire repos og låst af ADR-0001…0005.
> Tags: **[repo]** = fundet i repo · **[inferred]** = udledt · **[anbef]** = anbefaling.

---

## 1. Mål-arkitektur

Tre planer + managed services. Princip (ADR-0005): **Biyocon = kroppen, Python-sidecar = hjernen.**

```
┌─────────────────────────── BROWSER ───────────────────────────┐
│ Biyocon tabletop UI (Next.js/React/Tailwind/shadcn)  [repo]    │
│  • deltager-/agentpladser  • status: idle/listening/           │
│    thinking/speaking  • command palette                        │
│  • LiveKit client SDK (media)   • WS/SSE client (agent-events)  │
└───────────────┬─────────────────────────────┬─────────────────┘
                │ media (WebRTC)               │ WS/SSE + REST
                ▼                              ▼
        ┌──────────────┐         ┌──────────────────────────────┐
        │ LiveKit Cloud│         │ Biyocon BFF (Next.js server)  │
        │ (EU, testdata)│        │  • auth/session (Teams-ready) │
        │  ADR-0003     │        │  • LiveKit token minting      │
        └──────────────┘        │  • room/participant state     │
                                 │  • proxy → sidecar, stream →  │
                                 │    client                     │
                                 └───────────────┬──────────────┘
                                   HTTP + SSE (Agent Event Contract)
                                                 ▼
                  ┌────────────────────────────────────────────────┐
                  │ Python Agent Sidecar (FastAPI)  [odysseus-mønstret]│
                  │  • AgentProfile loader (custom-format)  [repo]   │
                  │  • MeetingAgentInstance lifecycle                │
                  │  • RAG retrieval (Chroma/pgvector)               │
                  │  • privat + fælles brain (memory)                │
                  │  • tool dispatcher + policy + owner-scoping      │
                  │  • audit  • STT/TTS-orkestrering                 │
                  │  • provider-adapters (LLM/TTS/STT)               │
                  └───────┬───────────────┬───────────────┬─────────┘
                          ▼               ▼               ▼
                   Azure Neural TTS   Whisper STT    LLM (OpenAI/
                   (EU)  ADR-0004     ADR-0004       Anthropic/Ollama)
                          │
                   App DB (Postgres) + Vector DB (Chroma/pgvector)
```

**Ansvarsfordeling**

| Plan | Ejer | Ejer IKKE |
|---|---|---|
| Biyocon UI | Visuel mødeoplevelse, room-rendering, agent-status-visning | Intelligens, RAG, memory |
| Biyocon BFF | Auth/session, LiveKit-tokens, room/participant-state, event-streaming, sidecar-proxy | Agent-logik, model-kald |
| Python sidecar | Agent-runtime, RAG, brain, tool-policy, owner-scoping, audit, STT/TTS-orkestrering | UI, LiveKit-room-state |
| Managed | Media (LiveKit), TTS (Azure), STT (Whisper), LLM | — |

**Arkitekturregler:** kontrakt-først (afsnit 2); adapter-baserede providers (media/voice/LLM udskiftelige → self-host-exit); owner-scoping på hver entitet; audit på hver agent-handling; kun testdata i MVP.

## 2. Agent Event Contract

Stabil kontrakt, så sidecar'en er udskiftelig (første demo må stubbe den i TS). To kanaler:

- **Client ↔ BFF:** WS (bidirektionel) eller SSE (server→client events) + REST (commands).
- **BFF ↔ Sidecar:** `POST /agent/respond` (command) + `GET /agent/events/{meetingId}` (SSE-stream). `[anbef]`

**Envelope (alle beskeder):**
```ts
type AgentEvent = {
  type: string            // se nedenfor
  meetingId: string
  agentInstanceId?: string
  ts: string              // ISO-8601
  correlationId: string
  payload: unknown
}
```

**Server/sidecar → client:**
| type | payload |
|---|---|
| `agent.status` | `{ status: "idle"\|"listening"\|"thinking"\|"speaking" }` |
| `agent.message.delta` | `{ text }` (streaming-chunk) |
| `agent.message.final` | `{ text, citations?: KnowledgeRef[] }` |
| `agent.audio` | `{ audioUrl \| chunk, format }` (TTS) |
| `agent.action` | `{ kind: "decision"\|"action_item", data }` |
| `agent.tool.approval_request` | `{ toolId, args, reason }` (human-in-the-loop) |
| `meeting.summary` | `{ summary, decisions[], actionItems[] }` |
| `audit.event` | `{ actor, action, target }` |

**Client → BFF → sidecar (commands):**
| command | payload |
|---|---|
| `agent.add` | `{ agentProfileId, role }` |
| `agent.respond` | `{ agentInstanceId, prompt?, knowledgeScopeId }` |
| `knowledgeScope.set` | `{ sources: SourceRef[] }` |
| `tool.approve` | `{ approvalId, approved }` |

## 3. Datamodel

Owner-scoping på alt runtime: hver entitet bærer `tenantId` + `meetingId` (+ `agentInstanceId`/`ownerId`). **[repo]** odysseus' `Session.owner` bekræfter mønstret.

```ts
// Definition af en digital medarbejder — [repo] custom profile.md frontmatter
type AgentProfile = {
  id: string                  // "abdi-asis-produkt-manager"
  name: string                // "Abdi Asis"
  role: string                // "Technical Product Manager"
  category: string
  avatarRef: string           // -> AgentAvatar
  colorAccent: string         // "violet"  (matcher avatar style spec)
  status: "active" | "inactive"
  sourceRef?: string          // hvor system-prompten stammer fra
  primaryModels: string[]     // ["Codex","Kimi",...]
  skillRefs: string[]         // -> AgentSkill (by name)
  systemPrompt: string
  languageProfile?: string[]  // ["da-DK","en-US",...]
}

// [repo] custom skills.yaml: skills[] + capabilities[]
type AgentSkill = { id: string; capabilities: string[] }

// [ADR-0004]
type AgentVoiceProfile = {
  agentProfileId: string
  voiceProvider: "azure" | "elevenlabs" | "self_hosted"
  voiceId: string
  language: "da-DK" | "en-US" | string
  style?: string; speakingRate?: number; pitch?: number
  consentStatus: "standard_voice" | "cloned_voice_consent_pending" | "cloned_voice_approved"
  syntheticVoiceDisclosure: true
}

// [avatar style spec]
type AgentAvatar = {
  avatarImageRef: string
  avatarStyle: "illustrated"
  colorAccent?: string
  framing: "bust" | "three_quarter"
}

// egen/fælles brain  [inferred fra odysseus memory + glossar]
type AgentBrain = {
  id: string
  scope: { kind: "private"; agentInstanceId: string }
        | { kind: "shared"; meetingId: string }   // eller projectId
  memoryStoreRef: string
  retentionPolicy: string
}

// runtime-instans: en profil sat ind i et konkret møde  [inferred]
type MeetingAgentInstance = {
  agentInstanceId: string
  meetingId: string; tenantId: string
  agentProfileId: string
  role: string                 // rolle i netop dette møde
  voiceProfileId: string
  knowledgeScopeId: string
  privateBrainId: string
  status: "idle" | "listening" | "thinking" | "speaking"
  joinedAt: string
}

type Meeting = {
  meetingId: string; tenantId: string; ownerId: string
  livekitRoom: string
  sharedBrainId: string
  humanParticipants: string[]  // -> HumanParticipant
  agentInstances: string[]     // -> MeetingAgentInstance
  dataClassification: "test_only"   // MVP-constraint, ADR-0003
  createdAt: string
}

type HumanParticipant = {
  participantId: string; meetingId: string
  identity: string             // Teams-ready (Entra) senere
  livekitIdentity: string
}

// videnscope: hvad en agent må tilgå i et møde  [inferred]
type KnowledgeScope = {
  knowledgeScopeId: string; meetingId: string; tenantId: string
  sources: SourceRef[]         // folderRef | uploadRef | connectorRef
}

type FileAccessGrant = {
  fileAccessGrantId: string; knowledgeScopeId: string
  agentInstanceId: string; resourceRef: string
  permission: "read"
  grantedBy: string; grantedAt: string; expiresAt?: string
}

type ToolPermission = {
  toolPermissionId: string
  agentInstanceId?: string; agentProfileId?: string
  toolId: string; allowed: boolean
  requiresApproval: boolean     // human-in-the-loop, ADR-0005 out-of-scope: ingen autonom exec
  policyRef?: string
}

type AuditEvent = {
  auditEventId: string; meetingId: string; tenantId: string
  actor: string                 // agentInstanceId | userId
  action: string; target?: string; payloadHash?: string
  ts: string
}
```

**Relationer:** `AgentProfile 1—* MeetingAgentInstance` · `Meeting 1—* MeetingAgentInstance` · `Meeting 1—1 sharedBrain` · `MeetingAgentInstance 1—1 {privateBrain, AgentVoiceProfile, KnowledgeScope}` · `KnowledgeScope 1—* FileAccessGrant` · `AgentProfile *—* AgentSkill`.

## 4. Dataflows

**A. Møde-livscyklus**
1. `opret møde` → BFF skaber `Meeting` (+ LiveKit-room, `sharedBrain`, `dataClassification: test_only`).
2. `tilføj menneskelig deltager` → `HumanParticipant` + LiveKit-token (BFF).
3. `tilføj digital medarbejder` (`agent.add`) → sidecar loader `AgentProfile` (custom-format) → opretter `MeetingAgentInstance` (+ privat brain, voiceProfile, knowledgeScope).
4. `vælg rolle` → sættes på `MeetingAgentInstance.role`.
5. `vælg projektmappe/videnscope` (`knowledgeScope.set`) → `KnowledgeScope.sources`.
6. `giv filadgang` → `FileAccessGrant` pr. ressource (auditeret).
7. `start møde` → media op via LiveKit.
8. `agent lytter/læser kontekst` → STT-transskript + RAG-retrieval over `KnowledgeScope` → `agent.status: thinking`.
9. `agent svarer` → LLM → `agent.message.delta/final` (tekst) → Azure TTS → `agent.audio` → `agent.status: speaking`.
10. `agent genererer actions` → `agent.action` (decision/action_item) → beslutningslog.
11. `mødet afsluttes` → `meeting.summary`.
12. `opsummering eksporteres`. Hver handling i 3–11 → `AuditEvent`.

**B. Voice/STT/TTS-pipeline**
```
Menneske taler → LiveKit audio-track
   → Whisper STT (server-side / LiveKit egress)  [ADR-0004]
   → transskript → sidecar-kontekst (+ RAG)
   → LLM → svar-tekst (agent.message.delta, streaming)
   → Azure Neural TTS, EU (agent.audio)  [ADR-0004]
   → afspilning i rummet
```
`[anbef]` MVP: afspil agent-audio **client-side** (simplest); senere publicér agenten som en LiveKit-track (agent = deltager med egen audio), hvilket også er forudsætningen for Teams media-bot (fase 4). Syntetisk-stemme-disclosure vises ved agentpladsen.

## 5. Fremtidig Teams-integrationsflade (fase 2+)

Designet ind nu, bygges senere (ADR-0002): Teams in-meeting app (sidepanel/tab) taler med **samme BFF**; Teams SSO (Entra ID) mappes til auth/session-laget; mødekontekst via Microsoft Graph; `HumanParticipant.identity` gøres Entra-baseret. Media-bot (fase 4) genbruger LiveKit-track-modellen fra pipeline B til at tale agent-audio direkte ind i et kørende Teams-møde. Ingen Teams-kode i MVP — kun en stabil auth/session- og event-kontrakt, der ikke skal omskrives.
