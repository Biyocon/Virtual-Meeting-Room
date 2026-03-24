# 📋 Product Requirements Document (PRD)
# AI Virtuelt Møderum — BiyoCon Digital Portal

**Version:** 1.0.0  
**Dato:** 24. marts 2026  
**Forfatter:** BiyoCon Product Team  
**Status:** Draft for Review  

---

## 📑 Indholdsfortegnelse

1. [Executive Summary](#1-executive-summary)
2. [Produktvision og Mål](#2-produktvision-og-mål)
3. [Brugerroller og Personas](#3-brugerroller-og-personas)
4. [Funktionelle Krav](#4-funktionelle-krav)
5. [User Stories og Acceptance Criteria](#5-user-stories-og-acceptance-criteria)
6. [UI/UX Specifikation](#6-uiux-specifikation)
7. [Teknisk Arkitektur](#7-teknisk-arkitektur)
8. [Data Model og API](#8-data-model-og-api)
9. [AI Integration](#9-ai-integration)
10. [Sikkerhed og Compliance](#10-sikkerhed-og-compliance)
11. [Faseplan og Milestones](#11-faseplan-og-milestones)
12. [Success Metrics og KPI'er](#12-success-metrics-og-kpier)
13. [Risici og Mitigering](#13-risici-og-mitigering)
14. [Appendix](#14-appendix)

---

## 1. Executive Summary

### 1.1 Produktoversigt

**AI Virtuelt Møderum** er et intelligent digitalt samarbejdsrum integreret i BiyoCon's interne PWA-platform. Modulet kombinerer:

- **Videomøder** via LiveKit/WebRTC med lav latenstid
- **Realtids-transkription** via OpenAI Whisper (>95% præcision)
- **AI-analyse** af nøglepointer, beslutninger, opgaver og sentiment
- **Samarbejdsværktøjer**: chat, whiteboard, noter og dokumentdeling
- **Automatisk dokumentation**: mødereferater, action items og søgbar historik

### 1.2 Problemstilling

| Problem | Konsekvens |
|---------|------------|
| Manuel notering under møder | Ufuldstændige referater, tabte beslutninger |
| Uklare action items | Manglende opfølgning, forsinkede projekter |
| Fragmenterede værktøjer | Kontekstskift, ineffektivitet |
| Ingen søgbar mødehistorik | Gentagelse af diskussioner, tabt viden |

### 1.3 Løsning

Et "intelligent møderum" hvor AI'en forstår, strukturerer og assisterer i realtid – fra mødestart til auto-genereret referat og opgaveliste.

### 1.4 Kerneværdi

> **"Fra møde til handling på under 60 sekunder efter mødet slutter."**

---

## 2. Produktvision og Mål

### 2.1 Vision Statement

*"At transformere møder fra passive informationsudvekslinger til strukturerede, handlingsorienterede samarbejdssessioner, hvor AI fungerer som en usynlig facilitator, der sikrer at ingen beslutning går tabt og alle opgaver følges op."*

### 2.2 Strategiske Mål

| Mål | Metric | Target |
|-----|--------|--------|
| Reducér tid brugt på mødeadministration | Timer/uge/bruger | -60% |
| Øg opfølgningsrate på action items | Completion rate | >85% |
| Forbedre mødeeffektivitet | NPS score | >70 |
| Reducér "what did we decide?" samtaler | Support tickets | -80% |

### 2.3 Scope

**In Scope:**
- Live videomøder (op til 16 deltagere)
- Realtids transkription og AI-analyse
- Samarbejdsværktøjer (chat, whiteboard, noter)
- Automatisk referat og opgavegenerering
- Mødeanalytics og KPI-tracking
- Semantisk søgning i mødehistorik

**Out of Scope (v1.0):**
- Ekstern gæsteadgang uden BiyoCon-konto
- Telefon-dial-in
- Breakout rooms
- Live streaming til >50 deltagere
- Custom AI model fine-tuning

---

## 3. Brugerroller og Personas

### 3.1 Rolledefinitioner

```
┌─────────────────────────────────────────────────────────────────┐
│                        RBAC Hierarki                            │
├─────────────────────────────────────────────────────────────────┤
│  ADMIN                                                          │
│    ├── Fuld systemadgang                                        │
│    ├── Bruger- og rolleadministration                          │
│    ├── Analytics og audit logs                                  │
│    └── Systemkonfiguration                                      │
│                                                                 │
│  HOST                                                           │
│    ├── Oprette og administrere møder                           │
│    ├── Invitere deltagere                                       │
│    ├── Mute/kick deltagere                                      │
│    ├── Starte/stoppe optagelse                                  │
│    └── Adgang til AI-indsigter og referat                       │
│                                                                 │
│  MEMBER                                                         │
│    ├── Deltage i møder                                          │
│    ├── Dele skærm (hvis tilladt)                               │
│    ├── Bruge chat/whiteboard/noter                             │
│    └── Se egne mødereferater                                    │
│                                                                 │
│  GUEST                                                          │
│    ├── Deltage i møder (read-only transcription)               │
│    ├── Chat-adgang                                              │
│    └── Ingen adgang til optagelser/historik                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Personas

#### Persona 1: "Projektlederen Maria" (Host)

| Attribut | Beskrivelse |
|----------|-------------|
| **Rolle** | Project Manager, Infrastruktur |
| **Alder** | 38 |
| **Tech-niveau** | Intermediate |
| **Pain Points** | Bruger 4+ timer/uge på mødenoter og opfølgningsmails |
| **Mål** | Fokusere på facilitering, ikke dokumentation |
| **Success Metric** | "Jeg har et færdigt referat klar 1 minut efter mødet" |

#### Persona 2: "Ingeniøren Anders" (Member)

| Attribut | Beskrivelse |
|----------|-------------|
| **Rolle** | Geoteknisk Ingeniør |
| **Alder** | 32 |
| **Tech-niveau** | Advanced |
| **Pain Points** | Glemmer beslutninger fra møder for 2 uger siden |
| **Mål** | Hurtigt finde "hvad besluttede vi om X?" |
| **Success Metric** | "Jeg kan søge og finde enhver tidligere beslutning" |

#### Persona 3: "Direktøren Henrik" (Admin)

| Attribut | Beskrivelse |
|----------|-------------|
| **Rolle** | Afdelingschef |
| **Alder** | 52 |
| **Tech-niveau** | Basic |
| **Pain Points** | Mangler overblik over mødeeffektivitet på tværs af teams |
| **Mål** | Data-drevet indsigt i mødekultur |
| **Success Metric** | "Jeg kan se hvilke teams har flest uafsluttede action items" |

#### Persona 4: "Konsulenten Eva" (Guest)

| Attribut | Beskrivelse |
|----------|-------------|
| **Rolle** | Ekstern rådgiver |
| **Alder** | 45 |
| **Tech-niveau** | Intermediate |
| **Pain Points** | Skal bede om referater efter hvert møde |
| **Mål** | Nemt deltage uden tekniske forhindringer |
| **Success Metric** | "Jeg kan joine et møde med ét klik" |

---

## 4. Funktionelle Krav

### 4.1 Feature Map

```
AI VIRTUELT MØDERUM
│
├── F1: Mødeoprettelse og Planlægning
│   ├── F1.1 Opret nyt møde
│   ├── F1.2 Agenda builder
│   ├── F1.3 Deltagerinvitation
│   ├── F1.4 Kalenderintegration
│   └── F1.5 Recurring meetings
│
├── F2: Live Mødesession
│   ├── F2.1 Video/audio streaming
│   ├── F2.2 Skærmdeling
│   ├── F2.3 Grid layouts (gallery/speaker/presentation)
│   ├── F2.4 Mødekontroller (mute/camera/share/leave)
│   └── F2.5 Lobby og device check
│
├── F3: Realtids Transkription
│   ├── F3.1 Live speech-to-text
│   ├── F3.2 Speaker diarization
│   ├── F3.3 Multi-language support
│   ├── F3.4 Custom vocabulary
│   └── F3.5 Timestamp markers
│
├── F4: AI Analyse og Indsigter
│   ├── F4.1 Key points extraction
│   ├── F4.2 Decision tracking
│   ├── F4.3 Action item detection
│   ├── F4.4 Sentiment analysis
│   └── F4.5 Risk identification
│
├── F5: Samarbejdsværktøjer
│   ├── F5.1 Real-time chat
│   ├── F5.2 Interactive whiteboard
│   ├── F5.3 Collaborative notes
│   ├── F5.4 Document sharing
│   └── F5.5 Reactions og polls
│
├── F6: Eftermøde Dokumentation
│   ├── F6.1 Auto-generated summary
│   ├── F6.2 Action item list
│   ├── F6.3 Decision log
│   ├── F6.4 Export (PDF/Markdown)
│   └── F6.5 Integration med Projects/Tasks
│
├── F7: Optagelser og Historik
│   ├── F7.1 Møde recording
│   ├── F7.2 Transkript playback
│   ├── F7.3 Semantic search
│   ├── F7.4 Meeting archive
│   └── F7.5 Retention policies
│
└── F8: Analytics og Rapportering
    ├── F8.1 Taletid per deltager
    ├── F8.2 Engagement metrics
    ├── F8.3 Action item follow-up rate
    ├── F8.4 Meeting efficiency score
    └── F8.5 Team/org dashboards
```

### 4.2 Detaljerede Feature Specs

#### F1: Mødeoprettelse og Planlægning

**F1.1 Opret nyt møde**

| Felt | Type | Validering | Default |
|------|------|------------|---------|
| Titel | String | Required, 3-100 chars | — |
| Beskrivelse | Text | Optional, max 2000 chars | — |
| Start tidspunkt | DateTime | Required, ≥ now | — |
| Varighed | Duration | 15min - 4h | 60 min |
| Sprog (transkription) | Select | da, en, de, sv, no | da |
| Optagelse | Boolean | — | false |
| Agenda items | Array | Max 20 items | [] |
| Deltagere | UserIds[] | Max 16 | [host] |

**Forretningsregler:**
- Host tildeles automatisk til opretteren
- Kalenderbegivenhed oprettes automatisk ved bekræftelse
- Påmindelser sendes 24h, 1h og 15min før mødestart

---

#### F2: Live Mødesession

**F2.1 Video/Audio Streaming**

| Krav | Specifikation |
|------|---------------|
| Max deltagere | 16 simultane video feeds |
| Video codec | VP8/VP9 med simulcast |
| Audio codec | Opus med noise suppression |
| Min båndbredde | 1.5 Mbps up/down |
| Latency target | <200ms |
| Fallback | Audio-only ved lav båndbredde |

**F2.3 Grid Layouts**

```
┌─────────────────────────────────────────────┐
│              GALLERY VIEW (4x4)             │
├──────────┬──────────┬──────────┬───────────┤
│    P1    │    P2    │    P3    │    P4     │
├──────────┼──────────┼──────────┼───────────┤
│    P5    │    P6    │    P7    │    P8     │
├──────────┼──────────┼──────────┼───────────┤
│    P9    │   P10    │   P11    │   P12     │
├──────────┼──────────┼──────────┼───────────┤
│   P13    │   P14    │   P15    │   P16     │
└──────────┴──────────┴──────────┴───────────┘

┌─────────────────────────────────────────────┐
│              SPEAKER VIEW                   │
├─────────────────────────────────────────────┤
│                                             │
│              ACTIVE SPEAKER                 │
│                (Large)                      │
│                                             │
├──────┬──────┬──────┬──────┬──────┬─────────┤
│  P2  │  P3  │  P4  │  P5  │  P6  │   ...   │
└──────┴──────┴──────┴──────┴──────┴─────────┘

┌─────────────────────────────────────────────┐
│           PRESENTATION VIEW                 │
├─────────────────────────────────────────────┤
│                                             │
│            SHARED SCREEN                    │
│               (80%)                         │
│                                             │
├─────────────────────────────────────────────┤
│  P1  │  P2  │  P3  │  P4  │  Speaker       │
└──────┴──────┴──────┴──────┴─────────────────┘
```

**F2.5 Lobby og Device Check**

Pre-join skærm med:
- Mikrofon-vælger med VU-meter
- Kamera-vælger med preview
- Speaker test-knap
- Netværkskvalitetsindikator
- Sprogvalg til transkription
- "Join as Host/Member/Guest" valg

---

#### F3: Realtids Transkription

**F3.1 Live Speech-to-Text**

| Parameter | Værdi |
|-----------|-------|
| Model | OpenAI Whisper Large v3 |
| Streaming | Ja, chunked audio |
| Chunk size | 5 sekunder |
| Latency | <500ms fra tale til tekst |
| Accuracy target | ≥95% WER på klare forhold |

**F3.2 Speaker Diarization**

- Automatisk speaker-detection baseret på audio fingerprinting
- Mapping til deltager-profiler via enrollment
- Fallback: "Ukendt taler" med tidsstempel
- Mulighed for manuel korrektion post-møde

**F3.3 Multi-Language Support**

| Prioritet | Sprog | ISO Code |
|-----------|-------|----------|
| P0 | Dansk | da |
| P0 | Engelsk | en |
| P1 | Tysk | de |
| P1 | Svensk | sv |
| P2 | Norsk | no |

---

#### F4: AI Analyse og Indsigter

**F4.1-F4.5 AI Output Schema**

```typescript
interface MeetingInsights {
  keyPoints: {
    id: string;
    text: string;
    timestamp: number;
    speaker?: string;
    confidence: number; // 0-1
  }[];
  
  decisions: {
    id: string;
    description: string;
    timestamp: number;
    participants: string[];
    status: 'final' | 'tentative' | 'reversed';
  }[];
  
  actionItems: {
    id: string;
    task: string;
    assignee?: string;
    dueDate?: Date;
    priority: 'high' | 'medium' | 'low';
    timestamp: number;
  }[];
  
  sentiment: {
    overall: number; // -1 to 1
    byParticipant: Record<string, number>;
    timeline: { timestamp: number; score: number }[];
  };
  
  risks: {
    id: string;
    description: string;
    severity: 'high' | 'medium' | 'low';
    timestamp: number;
  }[];
  
  openQuestions: {
    id: string;
    question: string;
    askedBy?: string;
    timestamp: number;
    resolved: boolean;
  }[];
}
```

**AI Processing Pipeline:**

```
Audio Stream → Whisper → Transcript Segments
                              ↓
                    Batch (every 60s or on pause)
                              ↓
                    GPT-4 Analysis Prompt
                              ↓
         ┌────────────────────┼────────────────────┐
         ↓                    ↓                    ↓
    Key Points          Decisions            Action Items
         ↓                    ↓                    ↓
                    Merge & Deduplicate
                              ↓
                    Real-time UI Update
                              ↓
                    Firestore Persistence
```

---

#### F5: Samarbejdsværktøjer

**F5.1 Real-time Chat**

| Feature | Beskrivelse |
|---------|-------------|
| Mentions | @username med notifikation |
| Threads | Reply-to-message |
| Reactions | Emoji reactions på beskeder |
| File sharing | Drag-drop, max 25MB |
| Link preview | Auto-unfurl for URLs |
| Search | Full-text i chat historik |

**F5.2 Interactive Whiteboard**

Baseret på Tldraw engine:

| Værktøj | Beskrivelse |
|---------|-------------|
| Pen | Frihåndstegning, farve/tykkelse |
| Shapes | Rektangel, cirkel, pil, linje |
| Text | Tekstbokse med formatering |
| Sticky notes | Farvekodet post-its |
| Image | Upload og placer billeder |
| Eraser | Slet elementer |
| Select | Flyt, resize, rotate |
| Laser pointer | Midlertidig markør (host) |

Synkronisering via CRDT (Yjs) for konfliktfri samarbejde.

**F5.3 Collaborative Notes**

- Rich-text editor (ProseMirror-baseret)
- Markdown support
- Heading struktur
- Checklists
- Code blocks
- @mentions til deltagere
- Real-time cursor visibility
- Version history

---

#### F6: Eftermøde Dokumentation

**F6.1 Auto-generated Summary**

Template struktur:

```markdown
# Mødereferat: {title}

**Dato:** {date}  
**Varighed:** {duration}  
**Deltagere:** {participants}  
**Facilitator:** {host}

---

## 📌 TL;DR
{3-sentence executive summary}

## 🎯 Nøglepointer
1. {key_point_1}
2. {key_point_2}
...

## ✅ Beslutninger
| # | Beslutning | Deltagere | Status |
|---|------------|-----------|--------|
| 1 | {decision} | {names}   | Final  |
...

## 📋 Opgaver
| Opgave | Ansvarlig | Deadline | Prioritet |
|--------|-----------|----------|-----------|
| {task} | {assignee}| {date}   | Høj       |
...

## ❓ Åbne Spørgsmål
- {question_1}
- {question_2}

## 🔗 Vedhæftninger
- [Whiteboard snapshot]({link})
- [Noter]({link})
- [Optagelse]({link})

---
*Genereret af BiyoCon AI Meeting Assistant*
```

**F6.4 Export Formater**

| Format | Indhold | Use Case |
|--------|---------|----------|
| PDF | Formatted referat | Formel dokumentation |
| Markdown | Raw text | Integration med wikis |
| JSON | Structured data | API/automation |
| Email | HTML summary | Deltager notifikation |

---

#### F7: Optagelser og Historik

**F7.1 Møde Recording**

| Aspekt | Specifikation |
|--------|---------------|
| Format | WebM (VP9 + Opus) |
| Kvalitet | 720p default, 1080p optional |
| Max varighed | 4 timer |
| Storage | Firebase Storage (S3-backed) |
| Retention | 90 dage default, konfigurerbar |
| Access | Kun host + admin (RBAC) |

**F7.3 Semantic Search**

```
User Query: "Hvad besluttede vi om budget til Q3?"
          ↓
    Query Embedding (text-embedding-3-large)
          ↓
    Pinecone Vector Search
          ↓
    Top-K relevant segments (k=5)
          ↓
    Context + GPT-4 Answer Generation
          ↓
    "I mødet d. 15/2 besluttede I at..."
    [Link til timestamp i optagelse]
```

---

#### F8: Analytics og Rapportering

**F8.1-F8.5 Metrics Dashboard**

```typescript
interface MeetingAnalytics {
  // Per møde
  participation: {
    speakingTimeByUser: Record<string, number>; // sekunder
    interactionCount: Record<string, number>;
    cameraOnTime: Record<string, number>;
  };
  
  engagement: {
    overallScore: number; // 0-100
    attentionDropoffs: { timestamp: number; count: number }[];
    questionCount: number;
    reactionCount: number;
  };
  
  efficiency: {
    agendaAdherence: number; // % af planlagte punkter dækket
    decisionsMade: number;
    actionItemsCreated: number;
    meetingOverrun: number; // minutter
  };
  
  // Aggregeret (team/org)
  trends: {
    avgMeetingDuration: number;
    avgParticipants: number;
    actionItemCompletionRate: number;
    meetingsPerWeek: number;
  };
}
```

**Visualiseringer (Recharts):**
- Taletid: Horizontal bar chart per deltager
- Engagement: Line chart over mødevarighed
- Trends: Area chart over tid
- Action items: Funnel (created → assigned → completed)

---

## 5. User Stories og Acceptance Criteria

### Epic 1: Mødeoprettelse

**US-1.1: Som host vil jeg oprette et nyt møde**

```gherkin
GIVEN jeg er logget ind som host eller admin
WHEN jeg navigerer til /meeting/new
AND udfylder titel, dato/tid, og deltagere
AND klikker "Opret møde"
THEN oprettes mødet i Firestore
AND deltagere modtager kalenderinvitation
AND jeg redirectes til mødedetaljer
```

**Acceptance Criteria:**
- [ ] Formvalidering viser inline fejl
- [ ] Minimum 1 deltager (host) påkrævet
- [ ] Kalender-integration fungerer (Google/Outlook)
- [ ] Bekræftelsesmail sendes til alle deltagere
- [ ] Møde vises i "Planlagte møder" liste

---

**US-1.2: Som host vil jeg tilføje en agenda**

```gherkin
GIVEN jeg opretter eller redigerer et møde
WHEN jeg tilføjer agenda-punkter med estimeret tid
THEN gemmes agenda med mødet
AND vises til deltagere ved mødestart
AND AI bruger agenda til at tracke fremdrift
```

---

### Epic 2: Live Session

**US-2.1: Som deltager vil jeg joine et møde**

```gherkin
GIVEN jeg har modtaget en mødeinvitation
WHEN jeg klikker på mødelinket
THEN ser jeg lobby med device check
AND kan vælge mikrofon/kamera/speaker
AND ser netværkskvalitet
WHEN jeg klikker "Join møde"
THEN connecter jeg til LiveKit room
AND ser video grid med andre deltagere
```

**Acceptance Criteria:**
- [ ] Device permissions håndteres gracefully
- [ ] Fallback til audio-only ved kamera-fejl
- [ ] Connection state vises tydeligt (connecting/connected/reconnecting)
- [ ] Max 16 deltagere enforces

---

**US-2.2: Som host vil jeg mute en deltager**

```gherkin
GIVEN jeg er host i et aktivt møde
WHEN jeg klikker på en deltagers video tile
AND vælger "Mute"
THEN mutes deltagerens mikrofon
AND deltager ser notifikation om mute
AND deltager kan selv unmute igen
```

---

**US-2.3: Som deltager vil jeg dele min skærm**

```gherkin
GIVEN jeg er i et aktivt møde
AND har screenshare permission (host/member)
WHEN jeg klikker "Share Screen"
THEN vises browser's native screen picker
WHEN jeg vælger en skærm/vindue
THEN ses min skærm af alle deltagere
AND layout skifter til presentation view
```

---

### Epic 3: Transkription

**US-3.1: Som deltager vil jeg se live transkription**

```gherkin
GIVEN jeg er i et aktivt møde med transkription aktiveret
WHEN deltagere taler
THEN vises tekst i transkriptions-panelet
AND tekst er tildelt korrekt taler
AND nye segmenter auto-scrolles ind
```

**Acceptance Criteria:**
- [ ] Latency <500ms fra tale til tekst
- [ ] Speaker labels vises (eller "Ukendt taler")
- [ ] Timestamps vises for hver segment
- [ ] Scroll-to-current fungerer
- [ ] Kan pause auto-scroll for at læse tilbage

---

### Epic 4: AI Indsigter

**US-4.1: Som host vil jeg se AI-genererede nøglepointer**

```gherkin
GIVEN transkription er aktiv
WHEN AI identificerer et key point
THEN vises det i "Indsigter" panelet
AND er tagget med timestamp og taler
AND kan jeg markere det som "vigtigt" eller "fjern"
```

---

**US-4.2: Som host vil jeg se action items**

```gherkin
GIVEN AI detecterer en opgave i samtalen
THEN vises opgaven i action items listen
AND foreslås en assignee baseret på kontekst
AND kan jeg redigere task/assignee/deadline
AND kan jeg tilføje til Projects-modulet
```

---

### Epic 5: Samarbejde

**US-5.1: Som deltager vil jeg sende chat-beskeder**

```gherkin
GIVEN jeg er i et aktivt møde
WHEN jeg skriver i chat-inputtet
AND trykker Enter eller Send
THEN vises beskeden for alle deltagere
AND timestampes med mit navn
```

---

**US-5.2: Som deltager vil jeg bruge whiteboard**

```gherkin
GIVEN whiteboard er åbent
WHEN jeg tegner/skriver
THEN synkroniseres ændringer til alle deltagere
AND kan andre se min cursor i real-time
```

---

### Epic 6: Eftermøde

**US-6.1: Som host vil jeg generere et referat**

```gherkin
GIVEN mødet er afsluttet
WHEN jeg navigerer til /meeting/:id/summary
THEN ser jeg auto-genereret referat
AND kan redigere inden deling
AND kan eksportere som PDF/Markdown
AND kan sende til deltagere via email
```

**Acceptance Criteria:**
- [ ] Referat genereres inden 60 sekunder
- [ ] Alle beslutninger og action items inkluderet
- [ ] Whiteboard snapshot vedhæftet
- [ ] Links til optagelse og transkript
- [ ] PDF formatering er professionel

---

### Epic 7: Historik og Søgning

**US-7.1: Som bruger vil jeg søge i tidligere møder**

```gherkin
GIVEN jeg er på /meeting/recordings
WHEN jeg søger "budget Q3"
THEN returneres relevante møder/segmenter
AND vises med kontekst og timestamp
AND kan jeg klikke for at springe til det sted
```

---

### Epic 8: Analytics

**US-8.1: Som admin vil jeg se møde-analytics**

```gherkin
GIVEN jeg er admin
WHEN jeg navigerer til /meeting/analytics
THEN ser jeg dashboards med KPI'er
AND kan filtrere på team/periode
AND kan eksportere data
```

---

## 6. UI/UX Specifikation

### 6.1 Design System: Banedanmark Tema

#### Farvepalette

| Rolle | Farve | HEX | RGB | CSS Variable |
|-------|-------|-----|-----|--------------|
| **Primary Background** | Petrol-grøn | `#004E51` | 0, 78, 81 | `--bdk-petrol` |
| **Primary Dark** | Petrol mørk | `#003638` | 0, 54, 56 | `--bdk-petrol-dark` |
| **Primary 50%** | Petrol 50% | `#80A6A8` | 128, 166, 168 | `--bdk-petrol-50` |
| **Primary 20%** | Petrol 20% | `#CCE0E1` | 204, 224, 225 | `--bdk-petrol-20` |
| **Text Primary** | Koks-grå | `#323232` | 50, 50, 50 | `--bdk-gray` |
| **Text 50%** | Koks 50% | `#989898` | 152, 152, 152 | `--bdk-gray-50` |
| **Accent Primary** | Mint/Turkis | `#43FFC8` | 67, 255, 200 | `--bdk-mint` |
| **Accent Secondary** | Gul | `#FFFF66` | 255, 255, 102 | `--bdk-yellow` |
| **Accent Tertiary** | Pink | `#FFC8C8` | 255, 200, 200 | `--bdk-pink` |

#### CSS Variables

```css
:root {
  /* Banedanmark Primary */
  --bdk-petrol: #004E51;
  --bdk-petrol-dark: #003638;
  --bdk-petrol-50: #80A6A8;
  --bdk-petrol-20: #CCE0E1;
  
  /* Banedanmark Neutrals */
  --bdk-gray: #323232;
  --bdk-gray-50: #989898;
  --bdk-gray-20: #D9D9D9;
  
  /* Banedanmark Accents */
  --bdk-mint: #43FFC8;
  --bdk-mint-50: #A1FFDF;
  --bdk-mint-20: #D9FFF2;
  --bdk-yellow: #FFFF66;
  --bdk-yellow-50: #FFFFB3;
  --bdk-pink: #FFC8C8;
  --bdk-pink-50: #FFE4E4;
  
  /* Semantic */
  --color-success: var(--bdk-mint);
  --color-warning: var(--bdk-yellow);
  --color-error: #EF4444;
  --color-info: var(--bdk-petrol-50);
}
```

#### Typografi

| Element | Font | Weight | Size | Line Height |
|---------|------|--------|------|-------------|
| H1 | Segoe UI | Semibold | 32px | 1.2 |
| H2 | Segoe UI | Semibold | 24px | 1.3 |
| H3 | Segoe UI | Medium | 20px | 1.4 |
| Body | Segoe UI | Regular | 16px | 1.5 |
| Small | Segoe UI | Regular | 14px | 1.4 |
| Caption | Segoe UI | Regular | 12px | 1.3 |

*Note: Noir No1 bruges til grafiske produktioner (ikke UI).*

---

### 6.2 Meeting Room Layout

#### Overordnet Struktur

```
┌─────────────────────────────────────────────────────────────────┐
│                         HEADER                                  │
│  [Logo]  AI Strategy Meeting  Duration: 45:23    [4 Part.] [⚙] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐                           ┌─────────────┐    │
│   │ Participant │                           │ Participant │    │
│   │    (LEFT)   │                           │   (RIGHT)   │    │
│   └─────────────┘                           └─────────────┘    │
│                                                                 │
│              ┌─────────────────────────┐                       │
│              │      SCREEN SHARE       │                       │
│              │         PANEL           │                       │
│              │                         │                       │
│              └─────────────────────────┘                       │
│                                                                 │
│              ┌─────────────┐                                   │
│              │ Participant │                                   │
│              │  (BOTTOM)   │                                   │
│              └─────────────┘                                   │
│                                                                 │
│   ┌─────────────┐                           ┌─────────────┐    │
│   │ Participant │                           │ SIDEBAR     │    │
│   │    (TOP)    │                           │ (collapsible│    │
│   └─────────────┘                           │  320px)     │    │
│                                              │ • Chat      │    │
│                                              │ • Particip. │    │
│                                              │ • Notes     │    │
│                                              │ • AI Insight│    │
│                                              └─────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│                       CONTROL BAR                               │
│        [🎥 Video]  [🎤 Audio]  [💬 Chat]  [❌ Leave]           │
└─────────────────────────────────────────────────────────────────┘
```

#### Header Component

```tsx
interface MeetingHeader {
  container: "bg-[#004E51]/50 rounded-xl p-4 backdrop-blur-sm";
  left: {
    title: "text-white text-xl font-semibold";
    duration: "text-[#CCE0E1] text-sm";
  };
  right: {
    participantBtn: "bg-[#43FFC8]/20 border-[#43FFC8]/30 text-white rounded-full";
    iconBtns: "bg-white/10 hover:bg-[#43FFC8]/30 rounded-full p-2";
  };
}
```

#### Meeting Area

```tsx
interface MeetingArea {
  container: "flex-1 bg-[#80A6A8]/20 rounded-xl relative overflow-hidden";
  
  gridBackground: {
    pattern: "radial-gradient(circle, rgba(67,255,200,0.15) 1px, transparent 1px)";
    size: "30px 30px";
    opacity: "20%";
  };
  
  circularOverlays: {
    outer: "w-[80%] h-[80%] rounded-full bg-[#43FFC8]/10";
    inner: "w-[90%] h-[90%] rounded-full bg-[#43FFC8]/5";
  };
}
```

#### Screen Share Panel

```tsx
interface ScreenSharePanel {
  container: "bg-[#004E51]/60 backdrop-blur-sm rounded-lg border-[#43FFC8]/30";
  
  header: {
    background: "bg-[#004E51]/70";
    trafficLights: {
      close: "bg-[#FFC8C8]";  // Pink
      minimize: "bg-[#FFFF66]";  // Yellow
      maximize: "bg-[#43FFC8]";  // Mint
    };
    tabs: {
      active: "bg-[#43FFC8] text-[#004E51]";
      inactive: "text-[#CCE0E1] hover:bg-[#43FFC8]/20";
    };
  };
  
  content: {
    uploadIcon: "text-white w-10 h-10";
    heading: "text-white text-xl font-medium";
    description: "text-[#CCE0E1] text-sm";
    modePills: {
      active: "bg-[#43FFC8] text-[#004E51]";
      inactive: "bg-[#80A6A8]/50 text-white";
    };
    actionBtns: "bg-[#43FFC8]/20 border-[#43FFC8]/30 text-white";
  };
}
```

#### Participant Cards

```tsx
interface ParticipantCard {
  container: "bg-[#004E51]/90 backdrop-blur-sm p-3 rounded-lg w-64 border-[#43FFC8]/20";
  
  avatar: {
    image: "w-12 h-12 rounded-full ring-2 ring-[#43FFC8]/30";
    aiBadge: "bg-[#43FFC8] text-[#004E51] text-xs font-bold px-1.5 rounded-full";
  };
  
  info: {
    name: "text-white font-medium";
    role: "text-[#CCE0E1] text-xs";
    company: "text-[#80A6A8] text-xs";
    aiModel: "text-[#43FFC8] text-xs";
    modelBadge: "bg-[#FFFF66]/20 text-[#FFFF66] px-1.5 rounded";
  };
  
  actions: {
    icons: "text-[#CCE0E1] hover:text-[#43FFC8]";
  };
  
  positions: {
    top: { top: "10%", left: "50%", transform: "translateX(-50%)" };
    left: { top: "50%", left: "10%", transform: "translateY(-50%)" };
    right: { top: "50%", right: "10%", transform: "translateY(-50%)" };
    bottom: { bottom: "10%", left: "50%", transform: "translateX(-50%)" };
  };
}
```

#### Control Bar

```tsx
interface ControlBar {
  container: "bg-[#004E51]/70 backdrop-blur-sm rounded-full px-6 py-2 border-[#43FFC8]/20";
  
  buttons: {
    default: "bg-[#43FFC8]/20 border-[#43FFC8]/30 text-white px-4 py-2 rounded-full";
    hover: "hover:bg-[#43FFC8]/40";
    active: "bg-[#43FFC8] text-[#004E51]";
    danger: "bg-red-500/20 border-red-500/30 text-red-400 hover:bg-red-500/40";
  };
}
```

#### Sidebar Panels

```tsx
interface SidebarPanels {
  container: "w-80 bg-[#004E51]/80 backdrop-blur-sm border-l border-[#43FFC8]/20";
  
  tabs: {
    active: "bg-[#43FFC8] text-[#004E51]";
    inactive: "text-[#CCE0E1]";
  };
  
  panels: {
    chat: {
      messages: "bg-[#003638]/50 rounded-lg p-2";
      input: "bg-[#004E51] border-[#43FFC8]/30";
    };
    participants: {
      item: "hover:bg-[#43FFC8]/10";
      status: {
        online: "bg-[#43FFC8]";
        muted: "bg-[#FFFF66]";
        offline: "bg-[#989898]";
      };
    };
    notes: {
      editor: "bg-[#003638]/30";
    };
    insights: {
      card: "bg-[#43FFC8]/10 border-[#43FFC8]/20 rounded-lg p-3";
      badge: {
        keyPoint: "bg-[#43FFC8]/20 text-[#43FFC8]";
        decision: "bg-[#FFFF66]/20 text-[#FFFF66]";
        action: "bg-[#FFC8C8]/20 text-[#FFC8C8]";
      };
    };
  };
}
```

---

### 6.3 Page Layouts

#### /meeting/new (Opret møde)

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Tilbage                              Opret nyt møde           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Mødetitel *                                               │  │
│  │ ┌─────────────────────────────────────────────────────┐   │  │
│  │ │ Strategimøde Q3                                     │   │  │
│  │ └─────────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │ Beskrivelse                                               │  │
│  │ ┌─────────────────────────────────────────────────────┐   │  │
│  │ │ Gennemgang af Q3 strategi og milepæle...           │   │  │
│  │ └─────────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │ Dato og tid *                                             │  │
│  │ ┌────────────────┐  ┌──────────┐  ┌──────────┐           │  │
│  │ │ 24/03/2026    │  │ 14:00    │  │ 60 min   │           │  │
│  │ └────────────────┘  └──────────┘  └──────────┘           │  │
│  │                                                           │  │
│  │ Sprog (transkription)                                     │  │
│  │ ┌─────────────────────────────────────────────────────┐   │  │
│  │ │ 🇩🇰 Dansk                                     ▼    │   │  │
│  │ └─────────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │ ☑ Optag mødet                                            │  │
│  │ ☑ Aktivér AI-transkription                               │  │
│  │                                                           │  │
│  │ ────────────────────────────────────────────────────────  │  │
│  │                                                           │  │
│  │ Deltagere                                                 │  │
│  │ ┌─────────────────────────────────────────────────────┐   │  │
│  │ │ 🔍 Søg efter kollegaer...                          │   │  │
│  │ └─────────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │ Valgte deltagere:                                         │  │
│  │ [Maria Hansen ×] [Anders Nielsen ×] [+]                  │  │
│  │                                                           │  │
│  │ ────────────────────────────────────────────────────────  │  │
│  │                                                           │  │
│  │ Agenda                                                    │  │
│  │ 1. ┌──────────────────────────┐ ┌──────┐ [×]            │  │
│  │    │ Velkommen og intro       │ │ 5min │                 │  │
│  │    └──────────────────────────┘ └──────┘                 │  │
│  │ 2. ┌──────────────────────────┐ ┌──────┐ [×]            │  │
│  │    │ Q3 mål gennemgang        │ │ 20min│                 │  │
│  │    └──────────────────────────┘ └──────┘                 │  │
│  │ [+ Tilføj punkt]                                         │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│                                 [Annuller]  [✓ Opret møde]     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### /meeting/:id/lobby (Pre-join)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    Strategimøde Q3                              │
│                    14:00 - 15:00                                │
│                    4 deltagere venter                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              ┌─────────────────────────────┐                    │
│              │                             │                    │
│              │     [Camera Preview]        │                    │
│              │                             │                    │
│              │         👤                  │                    │
│              │                             │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
│              Mikrofon                                           │
│              ┌─────────────────────────────┐                    │
│              │ 🎤 MacBook Pro Microphone ▼ │                    │
│              └─────────────────────────────┘                    │
│              [████████░░░░░░░░] VU Meter                       │
│                                                                 │
│              Kamera                                             │
│              ┌─────────────────────────────┐                    │
│              │ 📹 FaceTime HD Camera    ▼ │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
│              Højtaler                                           │
│              ┌─────────────────────────────┐                    │
│              │ 🔊 MacBook Pro Speakers  ▼ │                    │
│              └─────────────────────────────┘                    │
│              [🔊 Test lyd]                                      │
│                                                                 │
│              Netværk: ████████████░░░ Fremragende              │
│                                                                 │
│              ────────────────────────────────                   │
│                                                                 │
│              Transkription sprog                                │
│              ┌─────────────────────────────┐                    │
│              │ 🇩🇰 Dansk                ▼ │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
│                                                                 │
│              ┌─────────────────────────────┐                    │
│              │      Join som Member        │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
│              [Join uden kamera] [Join uden lyd]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### /meeting/:id/summary (Eftermøde)

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Til møder                         Mødereferat                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Strategimøde Q3                                                │
│  ──────────────────────────────────────────────────────────     │
│  📅 24. marts 2026  ⏱️ 58 min  👥 4 deltagere                  │
│                                                                 │
│  [📥 Download PDF] [📧 Send til deltagere] [📋 Kopiér link]    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📌 TL;DR                                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Q3 budget blev godkendt med 15% stigning. Team skal      │  │
│  │ levere projektplan inden 1. april. Næste møde 7. april.  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  🎯 Nøglepointer                                                │
│  • Budget for Q3 er fastsat til 2.4M DKK                       │
│  • Ny medarbejder starter 15. april                            │
│  • Kundemøde med Acme Corp rykkes til maj                      │
│                                                                 │
│  ✅ Beslutninger                                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Budget godkendt                     Final    [🔗]     │   │
│  │ 2. Projektstrategi fastholdes          Final    [🔗]     │   │
│  │ 3. Outsourcing afventer analyse        Tentativ [🔗]     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📋 Opgaver                                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ☐ Udarbejd projektplan      @Maria    1. apr  Høj  [→]  │   │
│  │ ☐ Book kundemøde            @Anders   15. apr Med  [→]  │   │
│  │ ☐ Send velkomstmail         @HR       10. apr Lav  [→]  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  [Synk alle til Projects →]                                     │
│                                                                 │
│  ❓ Åbne spørgsmål                                              │
│  • Hvad er timeline for IT-migration?                          │
│  • Skal vi involvere eksterne konsulenter?                     │
│                                                                 │
│  📊 Sentiment                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Graph: Sentiment over tid - generelt positiv]           │  │
│  │ Overall: 😊 Positiv (0.72)                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  🔗 Vedhæftninger                                               │
│  • [📹 Optagelse (58:23)]                                      │
│  • [📝 Transkript]                                              │
│  • [🎨 Whiteboard snapshot]                                    │
│  • [📄 Delte dokumenter (2)]                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.4 Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | <640px | Sidebar hidden, bottom sheet modals, stacked layout |
| Tablet | 640-1024px | Collapsible sidebar, 2-column grid |
| Desktop | >1024px | Full layout, persistent sidebar |

### 6.5 Accessibility (WCAG 2.1 AA)

| Krav | Implementation |
|------|----------------|
| Kontrast | Min 4.5:1 for tekst, 3:1 for UI |
| Fokus | Synlig fokusring (mint outline) |
| Keyboard | Tab navigation, Enter/Space activation |
| Screen reader | ARIA labels på alle interaktive elementer |
| Reduced motion | `prefers-reduced-motion` respekteres |
| Target size | Min 44x44px for touch targets |

---

## 7. Teknisk Arkitektur

### 7.1 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (PWA)                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Next.js 14 + App Router + TypeScript                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ Tailwind│ │ shadcn/ │ │ LiveKit │ │ Recharts│       │   │
│  │  │   CSS   │ │   ui    │ │ Client  │ │         │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │ Service Worker  │ │    IndexedDB    │               │   │
│  │  │    (Workbox)    │ │  (Offline data) │               │   │
│  │  └─────────────────┘ └─────────────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FIREBASE PLATFORM                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   Firebase  │ │  Firestore  │ │   Cloud     │               │
│  │    Auth     │ │  Database   │ │  Storage    │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│  ┌─────────────────────────────────────────────┐               │
│  │            Cloud Functions                   │               │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │               │
│  │  │ LiveKit │ │ Whisper │ │   AI    │       │               │
│  │  │ Tokens  │ │ Stream  │ │ Insights│       │               │
│  │  └─────────┘ └─────────┘ └─────────┘       │               │
│  └─────────────────────────────────────────────┘               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
│     LiveKit     │ │   OpenAI    │ │  Pinecone   │
│   Cloud/SFU     │ │  Whisper +  │ │  Vector DB  │
│    (WebRTC)     │ │    GPT-4    │ │             │
└─────────────────┘ └─────────────┘ └─────────────┘
```

### 7.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | Next.js | 14.x | App Router, SSR, ISR |
| | TypeScript | 5.x | Type safety |
| | TailwindCSS | 3.4.x | Styling |
| | shadcn/ui | latest | UI components |
| | Lucide React | latest | Icons |
| | Recharts | latest | Charts/graphs |
| **PWA** | Workbox | 7.x | Service worker |
| | IndexedDB | native | Offline storage |
| **Realtime Video** | LiveKit | 1.x | WebRTC SFU |
| **Backend** | Firebase | 10.x | Auth, DB, Functions, Storage |
| **AI** | OpenAI Whisper | large-v3 | Transcription |
| | OpenAI GPT-4 | latest | Analysis, summaries |
| | text-embedding-3 | large | Embeddings |
| **Vector DB** | Pinecone | latest | Semantic search |

### 7.3 LiveKit Integration

```typescript
// lib/livekit.ts
interface LiveKitConfig {
  url: string; // wss://your-livekit-server.com
  apiKey: string;
  apiSecret: string;
  
  roomOptions: {
    adaptiveStream: true;
    dynacast: true;
    videoCaptureDefaults: {
      resolution: { width: 1280, height: 720 };
      facingMode: 'user';
    };
    audioCaptureDefaults: {
      echoCancellation: true;
      noiseSuppression: true;
      autoGainControl: true;
    };
  };
  
  publishOptions: {
    videoEncoding: {
      maxBitrate: 1_500_000;
      maxFramerate: 30;
    };
    simulcast: true;
    videoSimulcastLayers: [
      { width: 640, height: 360, encoding: { maxBitrate: 500_000 } },
      { width: 320, height: 180, encoding: { maxBitrate: 150_000 } },
    ];
  };
}

// Token generation (Cloud Function)
export async function generateLiveKitToken(
  roomName: string,
  participantId: string,
  role: 'host' | 'member' | 'guest'
): Promise<string> {
  const at = new AccessToken(apiKey, apiSecret, {
    identity: participantId,
    ttl: '4h',
  });
  
  at.addGrant({
    roomJoin: true,
    room: roomName,
    canPublish: role !== 'guest',
    canSubscribe: true,
    canPublishData: true,
    roomAdmin: role === 'host',
  });
  
  return at.toJwt();
}
```

### 7.4 AI Pipeline Architecture

```typescript
// services/ai-pipeline.ts
interface AIProcessingPipeline {
  // Stage 1: Audio capture
  audioCapture: {
    format: 'PCM 16-bit';
    sampleRate: 16000;
    channels: 1;
    chunkDuration: 5000; // ms
  };
  
  // Stage 2: Transcription
  transcription: {
    provider: 'openai';
    model: 'whisper-large-v3';
    language: string | 'auto';
    prompt?: string; // Domain-specific terms
    temperature: 0;
  };
  
  // Stage 3: Analysis (batched)
  analysis: {
    batchTrigger: 'every_60s' | 'on_silence' | 'manual';
    model: 'gpt-4-turbo';
    systemPrompt: `
      Du er en mødeassistent. Analysér følgende transkript og udtræk:
      1. Nøglepointer (max 5)
      2. Beslutninger (med deltagere og status)
      3. Opgaver (med ansvarlig og eventuel deadline)
      4. Åbne spørgsmål
      5. Sentiment (score -1 til 1)
      
      Svar i JSON format.
    `;
    maxTokens: 2000;
  };
  
  // Stage 4: Embedding & Storage
  embedding: {
    model: 'text-embedding-3-large';
    dimensions: 3072;
    chunkSize: 500; // tokens
    overlap: 50; // tokens
  };
  
  // Stage 5: Vector storage
  vectorStorage: {
    provider: 'pinecone';
    index: 'biyocon-meetings';
    namespace: 'transcripts';
    metadata: ['meetingId', 'timestamp', 'speaker'];
  };
}
```

### 7.5 Offline Architecture

```typescript
// lib/offline.ts
interface OfflineStrategy {
  // Cache strategies
  caching: {
    appShell: 'cache-first';
    api: 'network-first';
    assets: 'cache-first';
    meetingData: 'stale-while-revalidate';
  };
  
  // Offline capabilities
  capabilities: {
    viewMeetingList: true;
    viewPastMeetings: true;
    readTranscripts: true;
    viewSummaries: true;
    joinLiveMeeting: false; // Requires network
    editNotes: true; // Queued sync
    sendChat: true; // Queued sync
  };
  
  // Sync strategy
  sync: {
    trigger: 'online' | 'manual';
    conflictResolution: 'last-write-wins' | 'crdt';
    retryPolicy: {
      maxAttempts: 3;
      backoff: 'exponential';
    };
  };
  
  // IndexedDB schema
  stores: {
    meetings: { keyPath: 'id', indexes: ['userId', 'startAt'] };
    transcripts: { keyPath: 'id', indexes: ['meetingId', 'timestamp'] };
    insights: { keyPath: 'id', indexes: ['meetingId'] };
    pendingActions: { keyPath: 'id', autoIncrement: true };
  };
}
```

---

## 8. Data Model og API

### 8.1 Firestore Collections

```typescript
// Firestore Schema

// Collection: meetings
interface Meeting {
  id: string;
  title: string;
  description?: string;
  startAt: Timestamp;
  endAt?: Timestamp;
  duration: number; // minutes
  language: 'da' | 'en' | 'de' | 'sv' | 'no';
  status: 'scheduled' | 'live' | 'ended' | 'cancelled';
  
  hostUid: string;
  participantUids: string[];
  
  settings: {
    recording: boolean;
    transcription: boolean;
    aiInsights: boolean;
    allowScreenShare: 'host' | 'all' | 'none';
    allowChat: boolean;
    allowNotes: boolean;
    allowWhiteboard: boolean;
  };
  
  agenda: {
    id: string;
    title: string;
    duration: number; // minutes
    order: number;
  }[];
  
  liveKitRoom?: string;
  
  createdAt: Timestamp;
  updatedAt: Timestamp;
  createdBy: string;
}

// Subcollection: meetings/{id}/transcript
interface TranscriptSegment {
  id: string;
  text: string;
  speaker: string | null;
  speakerUid?: string;
  startMs: number;
  endMs: number;
  confidence: number;
  language: string;
  createdAt: Timestamp;
}

// Subcollection: meetings/{id}/insights
interface MeetingInsights {
  id: string; // 'current' for live, 'final' for ended
  
  keyPoints: {
    id: string;
    text: string;
    timestamp: number;
    speaker?: string;
    confidence: number;
    markedImportant: boolean;
  }[];
  
  decisions: {
    id: string;
    description: string;
    timestamp: number;
    participants: string[];
    status: 'final' | 'tentative' | 'reversed';
  }[];
  
  actionItems: {
    id: string;
    task: string;
    assignee?: string;
    assigneeUid?: string;
    dueDate?: Timestamp;
    priority: 'high' | 'medium' | 'low';
    status: 'pending' | 'in-progress' | 'completed';
    timestamp: number;
    projectTaskId?: string; // Link to Projects module
  }[];
  
  openQuestions: {
    id: string;
    question: string;
    askedBy?: string;
    timestamp: number;
    resolved: boolean;
    answer?: string;
  }[];
  
  risks: {
    id: string;
    description: string;
    severity: 'high' | 'medium' | 'low';
    timestamp: number;
    mitigated: boolean;
  }[];
  
  sentiment: {
    overall: number;
    byParticipant: Record<string, number>;
    timeline: { timestamp: number; score: number }[];
  };
  
  summary?: {
    tldr: string;
    fullSummary: string;
    generatedAt: Timestamp;
  };
  
  updatedAt: Timestamp;
}

// Subcollection: meetings/{id}/chat
interface ChatMessage {
  id: string;
  senderUid: string;
  senderName: string;
  text: string;
  type: 'text' | 'file' | 'reaction';
  replyTo?: string;
  attachments?: {
    name: string;
    url: string;
    type: string;
    size: number;
  }[];
  reactions?: Record<string, string[]>; // emoji -> userIds
  createdAt: Timestamp;
  editedAt?: Timestamp;
  deleted?: boolean;
}

// Subcollection: meetings/{id}/notes
interface CollaborativeNote {
  id: string;
  content: string; // Markdown
  authorUid: string;
  authorName: string;
  version: number;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

// Subcollection: meetings/{id}/whiteboard
interface WhiteboardState {
  id: string;
  data: string; // Tldraw serialized state
  thumbnail?: string; // Base64 preview
  updatedAt: Timestamp;
  updatedBy: string;
}

// Collection: recordings
interface Recording {
  id: string;
  meetingId: string;
  storagePath: string;
  duration: number; // seconds
  size: number; // bytes
  format: 'webm';
  resolution: '720p' | '1080p';
  status: 'processing' | 'ready' | 'error';
  transcriptLinked: boolean;
  createdAt: Timestamp;
  expiresAt: Timestamp; // Retention policy
}

// Collection: users (extended for meetings)
interface UserMeetingProfile {
  uid: string;
  displayName: string;
  email: string;
  photoURL?: string;
  role: 'admin' | 'member';
  
  meetingPreferences: {
    defaultLanguage: string;
    defaultCamera: boolean;
    defaultMic: boolean;
    notificationSettings: {
      email: boolean;
      push: boolean;
      reminderTimes: number[]; // minutes before
    };
  };
  
  speakerEnrollment?: {
    voiceprint: string; // Reference to audio fingerprint
    enrolledAt: Timestamp;
  };
  
  stats: {
    meetingsHosted: number;
    meetingsAttended: number;
    totalSpeakingTime: number; // seconds
    actionItemsAssigned: number;
    actionItemsCompleted: number;
  };
}

// Collection: analytics/meetings/{meetingId}
interface MeetingAnalytics {
  meetingId: string;
  
  participation: {
    [userId: string]: {
      speakingTime: number; // seconds
      interactionCount: number;
      cameraOnTime: number;
      joinedAt: Timestamp;
      leftAt?: Timestamp;
    };
  };
  
  engagement: {
    score: number; // 0-100
    chatMessages: number;
    reactions: number;
    questionsAsked: number;
    attentionDropoffs: { timestamp: number; count: number }[];
  };
  
  efficiency: {
    plannedDuration: number;
    actualDuration: number;
    agendaItemsCovered: number;
    agendaItemsTotal: number;
    decisionsCount: number;
    actionItemsCreated: number;
  };
  
  ai: {
    transcriptionAccuracy?: number;
    insightsGenerated: number;
    processingTime: number; // ms
    tokensUsed: number;
    cost: number; // USD
  };
}
```

### 8.2 API Endpoints (Cloud Functions)

```typescript
// functions/src/meetings.ts

// Meeting Management
POST   /api/meetings                    // Create meeting
GET    /api/meetings                    // List user's meetings
GET    /api/meetings/:id                // Get meeting details
PATCH  /api/meetings/:id                // Update meeting
DELETE /api/meetings/:id                // Cancel meeting

// Live Session
POST   /api/meetings/:id/join           // Get LiveKit token
POST   /api/meetings/:id/start          // Start meeting (host only)
POST   /api/meetings/:id/end            // End meeting (host only)

// Transcription
POST   /api/meetings/:id/transcription/start    // Start transcription
POST   /api/meetings/:id/transcription/stop     // Stop transcription
WS     /api/meetings/:id/transcription/stream   // WebSocket for audio

// AI Insights
POST   /api/meetings/:id/insights/generate      // Trigger analysis
GET    /api/meetings/:id/insights               // Get current insights
PATCH  /api/meetings/:id/insights/items/:itemId // Update item

// Summary
POST   /api/meetings/:id/summary/generate       // Generate final summary
GET    /api/meetings/:id/summary                // Get summary
POST   /api/meetings/:id/summary/export         // Export PDF/MD

// Recordings
GET    /api/recordings                          // List recordings
GET    /api/recordings/:id                      // Get recording
GET    /api/recordings/:id/url                  // Get signed URL
DELETE /api/recordings/:id                      // Delete recording

// Search
POST   /api/search/meetings                     // Semantic search
GET    /api/search/suggestions                  // Autocomplete

// Analytics
GET    /api/analytics/meetings/:id              // Single meeting
GET    /api/analytics/overview                  // Aggregated stats
GET    /api/analytics/export                    // Export data
```

### 8.3 Real-time Data Flow

```typescript
// hooks/useMeetingRealtime.ts
interface RealtimeSubscriptions {
  // Firestore listeners
  meeting: {
    path: 'meetings/:id';
    events: ['modified'];
    handler: (meeting: Meeting) => void;
  };
  
  transcript: {
    path: 'meetings/:id/transcript';
    events: ['added'];
    orderBy: ['startMs', 'asc'];
    limit: 100;
    handler: (segments: TranscriptSegment[]) => void;
  };
  
  insights: {
    path: 'meetings/:id/insights/current';
    events: ['modified'];
    handler: (insights: MeetingInsights) => void;
  };
  
  chat: {
    path: 'meetings/:id/chat';
    events: ['added', 'modified'];
    orderBy: ['createdAt', 'desc'];
    limit: 50;
    handler: (messages: ChatMessage[]) => void;
  };
  
  participants: {
    path: 'meetings/:id/participants';
    events: ['added', 'removed', 'modified'];
    handler: (participants: Participant[]) => void;
  };
}
```

---

## 9. AI Integration

### 9.1 Transcription Service

```typescript
// services/transcription.ts
interface TranscriptionService {
  config: {
    model: 'whisper-large-v3';
    language: string | 'auto';
    responseFormat: 'verbose_json';
    timestampGranularity: 'segment';
  };
  
  // Streaming implementation
  async startStream(meetingId: string, options: {
    language: string;
    customVocabulary?: string[];
  }): Promise<void>;
  
  async processAudioChunk(
    meetingId: string,
    audioData: ArrayBuffer
  ): Promise<TranscriptSegment[]>;
  
  async stopStream(meetingId: string): Promise<void>;
  
  // Post-processing
  async correctSpeakers(
    meetingId: string,
    segments: TranscriptSegment[],
    participants: Participant[]
  ): Promise<TranscriptSegment[]>;
}

// Implementation details
const WHISPER_CONFIG = {
  endpoint: 'https://api.openai.com/v1/audio/transcriptions',
  model: 'whisper-1', // or whisper-large-v3 for self-hosted
  
  // Streaming via chunked audio
  chunkDuration: 5000, // 5 seconds
  overlapDuration: 500, // 0.5 second overlap
  
  // Quality settings
  temperature: 0,
  compression_ratio_threshold: 2.4,
  no_speech_threshold: 0.6,
};
```

### 9.2 AI Analysis Service

```typescript
// services/ai-analysis.ts
interface AIAnalysisService {
  // Analysis prompts
  prompts: {
    keyPoints: string;
    decisions: string;
    actionItems: string;
    sentiment: string;
    summary: string;
  };
  
  // Processing
  async analyzeTranscript(
    transcript: string,
    context: {
      meetingTitle: string;
      agenda?: string[];
      participants: string[];
      previousDecisions?: string[];
    }
  ): Promise<MeetingInsights>;
  
  async generateSummary(
    meetingId: string,
    format: 'tldr' | 'full' | 'executive'
  ): Promise<string>;
  
  async extractActionItems(
    transcript: string,
    participants: Participant[]
  ): Promise<ActionItem[]>;
}

// GPT-4 System Prompt for Analysis
const ANALYSIS_SYSTEM_PROMPT = `
Du er en professionel mødeassistent for en dansk infrastrukturvirksomhed.
Din opgave er at analysere mødetranskripter og udtrække struktureret information.

REGLER:
1. Vær præcis og faktuel - udtræk kun hvad der faktisk blev sagt
2. Identificer beslutninger klart - skelne mellem "endelig" og "foreløbig"
3. For opgaver: find ansvarlig person hvis nævnt, ellers marker som "uafklaret"
4. Sentinel analyse skal være objektiv og baseret på ordvalg/tone
5. Svar ALTID på dansk

OUTPUT FORMAT:
Svar i valid JSON med følgende struktur:
{
  "keyPoints": [{ "text": string, "confidence": number }],
  "decisions": [{ "description": string, "status": "final"|"tentative", "participants": string[] }],
  "actionItems": [{ "task": string, "assignee": string|null, "priority": "high"|"medium"|"low" }],
  "openQuestions": [{ "question": string }],
  "sentiment": { "overall": number, "notes": string }
}
`;
```

### 9.3 Semantic Search Service

```typescript
// services/semantic-search.ts
interface SemanticSearchService {
  // Indexing
  async indexTranscript(
    meetingId: string,
    segments: TranscriptSegment[]
  ): Promise<void>;
  
  async indexInsights(
    meetingId: string,
    insights: MeetingInsights
  ): Promise<void>;
  
  // Searching
  async search(
    query: string,
    filters?: {
      userId?: string;
      dateRange?: { start: Date; end: Date };
      meetingIds?: string[];
    },
    options?: {
      topK?: number;
      minScore?: number;
    }
  ): Promise<SearchResult[]>;
  
  // Context retrieval
  async getRelevantContext(
    meetingId: string,
    topic: string
  ): Promise<ContextChunk[]>;
}

interface SearchResult {
  meetingId: string;
  meetingTitle: string;
  segment: {
    text: string;
    timestamp: number;
    speaker?: string;
  };
  score: number;
  highlights: string[];
}

// Pinecone configuration
const PINECONE_CONFIG = {
  index: 'biyocon-meetings',
  namespace: 'production',
  
  // Embedding settings
  embeddingModel: 'text-embedding-3-large',
  dimensions: 3072,
  
  // Chunking settings
  chunkSize: 500, // tokens
  chunkOverlap: 50,
  
  // Search settings
  defaultTopK: 5,
  minScore: 0.7,
};
```

### 9.4 AI Cost Estimation

| Service | Unit | Cost | Est. Monthly (100 meetings) |
|---------|------|------|----------------------------|
| Whisper | per minute | $0.006 | $36 (avg 60min/meeting) |
| GPT-4 Turbo | per 1K tokens | $0.01 in / $0.03 out | $150 |
| Embeddings | per 1K tokens | $0.0001 | $5 |
| Pinecone | per vector/month | $0.00002 | $20 |
| **Total** | | | **~$211/month** |

---

## 10. Sikkerhed og Compliance

### 10.1 Authentication & Authorization

```typescript
// lib/auth.ts
interface AuthConfig {
  providers: ['email', 'google', 'microsoft'];
  
  mfa: {
    required: 'admin' | 'all' | 'none';
    methods: ['authenticator', 'sms'];
  };
  
  session: {
    type: 'jwt';
    accessTokenTTL: '1h';
    refreshTokenTTL: '7d';
    rotation: true;
  };
  
  rbac: {
    roles: ['admin', 'host', 'member', 'guest'];
    
    permissions: {
      'meeting:create': ['admin', 'host', 'member'];
      'meeting:delete': ['admin', 'host'];
      'meeting:start': ['admin', 'host'];
      'meeting:end': ['admin', 'host'];
      'meeting:record': ['admin', 'host'];
      'participant:mute': ['admin', 'host'];
      'participant:kick': ['admin', 'host'];
      'recording:view': ['admin', 'host'];
      'recording:delete': ['admin'];
      'analytics:view': ['admin'];
      'analytics:export': ['admin'];
    };
  };
}

// Firestore Security Rules (excerpt)
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Meetings
    match /meetings/{meetingId} {
      allow read: if isAuthenticated() && 
        (isParticipant(meetingId) || isAdmin());
      allow create: if isAuthenticated() && 
        hasPermission('meeting:create');
      allow update: if isAuthenticated() && 
        (isHost(meetingId) || isAdmin());
      allow delete: if isAuthenticated() && 
        (isHost(meetingId) || isAdmin());
      
      // Subcollections
      match /transcript/{segmentId} {
        allow read: if isParticipant(meetingId);
        allow write: if false; // Server-only
      }
      
      match /chat/{messageId} {
        allow read: if isParticipant(meetingId);
        allow create: if isParticipant(meetingId) && 
          request.auth.uid == request.resource.data.senderUid;
      }
    }
    
    // Recordings - strict access
    match /recordings/{recordingId} {
      allow read: if isAuthenticated() && 
        (isRecordingOwner(recordingId) || isAdmin());
      allow write: if false; // Server-only
      allow delete: if isAdmin();
    }
  }
}
```

### 10.2 Data Privacy (GDPR)

```typescript
// lib/privacy.ts
interface GDPRCompliance {
  // Consent management
  consent: {
    recording: {
      required: true;
      prompt: 'before_join';
      storage: 'user_preferences';
    };
    transcription: {
      required: true;
      prompt: 'before_join';
      storage: 'user_preferences';
    };
    analytics: {
      required: false;
      prompt: 'settings';
      storage: 'user_preferences';
    };
  };
  
  // Data retention
  retention: {
    meetings: '2_years';
    recordings: '90_days';
    transcripts: '2_years';
    chat: '1_year';
    analytics: '2_years';
    auditLogs: '7_years';
  };
  
  // User rights
  rights: {
    access: {
      endpoint: '/api/user/data-export';
      format: 'json';
      timeframe: '30_days';
    };
    rectification: {
      endpoint: '/api/user/update';
      fields: ['displayName', 'email', 'preferences'];
    };
    erasure: {
      endpoint: '/api/user/delete';
      includes: ['meetings_hosted', 'chat_messages', 'notes'];
      excludes: ['aggregated_analytics'];
      timeframe: '30_days';
    };
    portability: {
      endpoint: '/api/user/export';
      formats: ['json', 'csv'];
    };
  };
  
  // Anonymization
  anonymization: {
    trigger: 'user_deletion' | 'retention_expiry';
    fields: ['speaker_names', 'user_ids'];
    preserves: ['aggregated_stats', 'anonymized_transcripts'];
  };
}
```

### 10.3 Encryption

| Data State | Method | Implementation |
|------------|--------|----------------|
| **In Transit** | TLS 1.3 | Firebase default + CloudFlare |
| **At Rest** | AES-256 | Firebase default encryption |
| **Video Streams** | DTLS-SRTP | LiveKit WebRTC |
| **Audio Chunks** | AES-256-GCM | Before sending to Whisper |
| **Stored Recordings** | AES-256 | Firebase Storage + KMS |

### 10.4 Audit Logging

```typescript
// services/audit.ts
interface AuditEvent {
  id: string;
  timestamp: Timestamp;
  
  actor: {
    uid: string;
    email: string;
    role: string;
    ip: string;
    userAgent: string;
  };
  
  action: AuditAction;
  resource: {
    type: 'meeting' | 'recording' | 'user' | 'settings';
    id: string;
    name?: string;
  };
  
  details: Record<string, any>;
  result: 'success' | 'failure';
  errorCode?: string;
}

type AuditAction =
  | 'meeting.create'
  | 'meeting.start'
  | 'meeting.end'
  | 'meeting.delete'
  | 'recording.start'
  | 'recording.stop'
  | 'recording.view'
  | 'recording.download'
  | 'recording.delete'
  | 'participant.join'
  | 'participant.leave'
  | 'participant.mute'
  | 'participant.kick'
  | 'transcription.start'
  | 'transcription.stop'
  | 'insights.generate'
  | 'summary.export'
  | 'user.login'
  | 'user.logout'
  | 'user.data_export'
  | 'user.data_delete'
  | 'settings.update';

// Audit log retention: 7 years (compliance)
// Storage: Firestore + BigQuery export (monthly)
```

---

## 11. Faseplan og Milestones

### 11.1 Fase Oversigt

```
┌─────────────────────────────────────────────────────────────────┐
│                      UDVIKLINGSFASER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1 ──────────────────────────────────────── 4 uger        │
│  │ Basis Live + UI Shell                                       │
│  │ • LiveKit integration                                        │
│  │ • Video grid layouts                                         │
│  │ • Mødekontroller                                             │
│  │ • Sidebar tabs (stub)                                        │
│  │ • App Shell integration                                      │
│  │                                                              │
│  FASE 2 ──────────────────────────────────────── 3 uger        │
│  │ Transkription                                                │
│  │ • Whisper streaming integration                              │
│  │ • Transkript-panel UI                                        │
│  │ • Speaker diarization                                        │
│  │ • Multi-language support                                     │
│  │                                                              │
│  FASE 3 ──────────────────────────────────────── 4 uger        │
│  │ AI Indsigter                                                 │
│  │ • GPT-4 analyse pipeline                                     │
│  │ • Real-time indsigter UI                                     │
│  │ • Action item detection                                      │
│  │ • Sentiment analysis                                         │
│  │                                                              │
│  FASE 4 ──────────────────────────────────────── 3 uger        │
│  │ Sammenfatning & Optagelser                                   │
│  │ • Auto-summary generation                                    │
│  │ • Summary view UI                                            │
│  │ • Recording management                                       │
│  │ • Export funktioner                                          │
│  │                                                              │
│  FASE 5 ──────────────────────────────────────── 3 uger        │
│  │ Analytics & Pinecone                                         │
│  │ • Møde-analytics dashboard                                   │
│  │ • Semantic search                                            │
│  │ • Historical context                                         │
│  │ • KPI tracking                                               │
│                                                                 │
│  TOTAL ─────────────────────────────────────── 17 uger         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 11.2 Detaljeret Faseplan

#### Fase 1: Basis Live + UI Shell (4 uger)

**Uge 1-2: LiveKit Integration**
- [ ] LiveKit account setup og konfiguration
- [ ] Cloud Function: Token generation med RBAC
- [ ] React hooks: `useLiveKit`, `useParticipants`, `useLocalMedia`
- [ ] Connection state management
- [ ] Error handling og reconnection logic

**Uge 2-3: Video Grid & Controls**
- [ ] VideoTile component med Banedanmark styling
- [ ] Grid layouts: Gallery, Speaker, Presentation
- [ ] Active speaker detection
- [ ] Control bar: Mute, Camera, Share, Leave
- [ ] Screen sharing implementation

**Uge 3-4: Meeting Room UI**
- [ ] Meeting header component
- [ ] Circular layout med participant cards
- [ ] Screen share panel
- [ ] Sidebar struktur (tabs)
- [ ] Lobby/device check screen
- [ ] App Shell integration

**Deliverables:**
- Fungerende video-møde med 4+ deltagere
- Alle grid layouts implementeret
- Skærmdeling virker
- Responsive design

---

#### Fase 2: Transkription (3 uger)

**Uge 5: Whisper Integration**
- [ ] Audio capture fra LiveKit
- [ ] Cloud Function: Whisper streaming endpoint
- [ ] WebSocket connection til audio streaming
- [ ] Chunk management og buffering

**Uge 6: Transkript UI**
- [ ] TranscriptPanel component
- [ ] Real-time segment rendering
- [ ] Auto-scroll med pause-on-hover
- [ ] Speaker labels og timestamps
- [ ] Search i transkript

**Uge 7: Speaker Diarization**
- [ ] Audio fingerprint enrollment flow
- [ ] Speaker mapping logic
- [ ] "Ukendt taler" fallback
- [ ] Manual correction UI
- [ ] Multi-language switcher

**Deliverables:**
- Live transkription med <500ms latency
- ≥95% accuracy på klare forhold
- Speaker identification
- Dansk + Engelsk support

---

#### Fase 3: AI Indsigter (4 uger)

**Uge 8-9: Analysis Pipeline**
- [ ] GPT-4 integration i Cloud Functions
- [ ] Batch processing logic (60s intervals)
- [ ] JSON parsing og validering
- [ ] Firestore persistence
- [ ] Error handling og retries

**Uge 10: Insights UI**
- [ ] InsightsPanel component
- [ ] KeyPoints list med timestamps
- [ ] Decisions tracker
- [ ] Action items med assignee
- [ ] Open questions list

**Uge 11: Sentiment & Polish**
- [ ] Sentiment analysis integration
- [ ] Sentiment timeline visualization
- [ ] Risk identification
- [ ] Manual editing af insights
- [ ] "Mark as important" funktion

**Deliverables:**
- Real-time AI indsigter
- Alle 5 insight-typer implementeret
- Editable insights
- Sentiment graf

---

#### Fase 4: Sammenfatning & Optagelser (3 uger)

**Uge 12: Summary Generation**
- [ ] Final summary prompt engineering
- [ ] TL;DR generation
- [ ] Full summary markdown output
- [ ] Post-meeting trigger (on end)

**Uge 13: Summary UI & Export**
- [ ] SummaryView page
- [ ] Editable summary sections
- [ ] PDF export (react-pdf)
- [ ] Markdown export
- [ ] Email to participants

**Uge 14: Recording Management**
- [ ] LiveKit recording API integration
- [ ] Recording list UI
- [ ] Playback med transcript-hopping
- [ ] Storage management
- [ ] Retention policy implementation

**Deliverables:**
- Auto-genereret referat inden 60s
- PDF/MD export
- Recording playback
- Synk til Projects

---

#### Fase 5: Analytics & Pinecone (3 uger)

**Uge 15: Analytics Dashboard**
- [ ] AnalyticsPage layout
- [ ] Speaking time chart (Recharts)
- [ ] Engagement metrics
- [ ] Action item funnel
- [ ] Team/org aggregation

**Uge 16: Semantic Search**
- [ ] Pinecone setup og indexing
- [ ] Embedding generation pipeline
- [ ] Search API endpoint
- [ ] Search UI med filters
- [ ] Result highlighting

**Uge 17: Polish & Launch Prep**
- [ ] Historical context retrieval
- [ ] Cross-meeting insights
- [ ] Performance optimization
- [ ] Documentation
- [ ] Beta testing

**Deliverables:**
- Komplet analytics dashboard
- Semantic search fungerer
- Historisk kontekst i nye møder
- Production-ready

---

### 11.3 Milestone Checklist

| Milestone | Dato | Kriterier |
|-----------|------|-----------|
| **M1: Video MVP** | Uge 4 | 4+ deltagere, alle layouts, skærmdeling |
| **M2: Transkription Live** | Uge 7 | <500ms latency, ≥95% WER, speakers |
| **M3: AI Indsigter Live** | Uge 11 | Key points, decisions, actions, sentiment |
| **M4: Referat Ready** | Uge 14 | Auto-summary, export, recordings |
| **M5: Full Feature** | Uge 17 | Analytics, search, production deploy |

---

## 12. Success Metrics og KPI'er

### 12.1 Product Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **Adoption** | | | |
| Weekly active users | 0 | 80% of org | Analytics |
| Meetings per user/week | 0 | 3+ | Analytics |
| AI features enabled | 0 | 90% | Settings |
| **Efficiency** | | | |
| Time to referat | Manual: 30min | <60 sec | Timer |
| Action item completion | Unknown | 85% | Project sync |
| Repeat discussions | Unknown | -50% | Survey |
| **Quality** | | | |
| Transcription accuracy | - | ≥95% | Sampling QA |
| Insight relevance | - | ≥85% | User feedback |
| User satisfaction | - | NPS >70 | Survey |
| **Technical** | | | |
| Video latency | - | <200ms | Monitoring |
| Transcript latency | - | <500ms | Monitoring |
| Uptime | - | 99.9% | Monitoring |

### 12.2 Business Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Time saved per week | (manual_time - ai_time) × users | 200+ hours/week |
| Meeting efficiency gain | (decisions + actions) / duration | +25% |
| Follow-up completion | completed_actions / total_actions | 85% |
| Knowledge retention | successful_searches / total_searches | 80% |

### 12.3 Tracking Implementation

```typescript
// analytics/events.ts
interface MeetingAnalyticsEvents {
  // Session events
  'meeting.started': { meetingId: string; participantCount: number };
  'meeting.ended': { meetingId: string; duration: number };
  'meeting.joined': { meetingId: string; role: string };
  
  // Feature usage
  'transcription.enabled': { meetingId: string; language: string };
  'insights.viewed': { meetingId: string; insightType: string };
  'summary.generated': { meetingId: string; generationTime: number };
  'summary.exported': { meetingId: string; format: string };
  
  // AI interactions
  'actionItem.created': { source: 'ai' | 'manual' };
  'actionItem.synced': { destination: 'projects' | 'tasks' };
  'search.performed': { query: string; resultCount: number };
  
  // User feedback
  'feedback.insight': { meetingId: string; helpful: boolean };
  'feedback.summary': { meetingId: string; rating: number };
}
```

---

## 13. Risici og Mitigering

### 13.1 Risk Matrix

| Risk | Sandsynlighed | Impact | Score | Mitigering |
|------|---------------|--------|-------|------------|
| **R1: Whisper latency** | Medium | High | 6 | Chunk optimization, fallback til batch |
| **R2: GPT-4 rate limits** | Medium | Medium | 4 | Queue system, caching, retry logic |
| **R3: LiveKit skalering** | Low | High | 3 | Cloud-hosted, auto-scaling |
| **R4: GDPR non-compliance** | Low | Critical | 4 | Legal review, consent flows, audit |
| **R5: User adoption** | Medium | High | 6 | Training, onboarding, champions |
| **R6: Cost overrun (AI)** | Medium | Medium | 4 | Usage monitoring, quotas, optimization |
| **R7: Browser compatibility** | Low | Medium | 2 | Testing matrix, polyfills |
| **R8: Offline sync conflicts** | Medium | Low | 2 | CRDT, conflict resolution UI |

### 13.2 Risk Details

#### R1: Whisper Latency

**Problem:** Streaming transcription may exceed 500ms target.

**Mitigering:**
1. Optimize audio chunking (5s chunks with 0.5s overlap)
2. Use dedicated GPU instance for Whisper
3. Implement client-side caching
4. Fallback: Batch processing hver 30s med "live preview" baseret på simple ASR

#### R5: User Adoption

**Problem:** Brugere fortsætter med gamle vaner (manuel notering, ingen AI).

**Mitigering:**
1. Onboarding tour ved første møde
2. "Champion program" med early adopters
3. Gamification: "Meeting efficiency score"
4. Management KPI: Team adoption rate
5. Automatisk "prøv AI" prompt efter 3 meetings uden

---

## 14. Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **SFU** | Selective Forwarding Unit - server der router video streams |
| **CRDT** | Conflict-free Replicated Data Type - synkroniseringsprotokol |
| **WER** | Word Error Rate - måleenhed for transkriptionspræcision |
| **Diarization** | Proces til at identificere hvem der taler hvornår |
| **Embedding** | Numerisk vektor-repræsentation af tekst |
| **Vector DB** | Database optimeret til similarity search |

### B. Reference Dokumenter

- [BiyoCon Technical Architecture](./03_Technical_Architecture.md)
- [UI Requirements](./04_UI_Requirements.md)
- [AI Integration Spec](./10_AI_Integration.md)
- [CRM Features](./13_CRM_Features.md)
- [Sitemap](./02_Sitemap.md)

### C. Design Assets

- Banedanmark Designguide 2021
- Figma: AI Meeting Room Components
- Icon set: Lucide React

### D. API Documentation Links

- [LiveKit Docs](https://docs.livekit.io/)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI GPT-4 API](https://platform.openai.com/docs/guides/gpt)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Firebase Docs](https://firebase.google.com/docs)

---

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Tech Lead | | | |
| UX Lead | | | |
| Security | | | |

---

*Document Version: 1.0.0*  
*Last Updated: 24. marts 2026*  
*Next Review: Ved fase 1 completion*
