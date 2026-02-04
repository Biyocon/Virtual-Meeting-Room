# Google AI Studio Masterprompt: AI Virtual Meeting Room

Dette dokument kondenserer projektets nuværende UI/design og teknologi (Next.js 15, App Router, Tailwind, shadcn/ui, lucide-react) samt en komplet masterprompt, der kan indsættes i https://aistudio.google.com/u/1/prompts/new_chat for at få en agent til at klone og udbygge løsningen som en fuld PWA. Promptsproget er dansk/engelsk blandet for klarhed og håndhæver integrationer til Microsoft Teams og Googles mødeprodukter (f.eks. Google Meet / Calendar / Drive).

## Projektsnapshot (fundet i koden)
- UI: Purple gradient baggrund med kort-baserede deltagere, hovedskærm, top-header og bundkontroller til video/audio/chat; skærmdeling vises i hovedkortet; aktiv taler-overlay i toppen.【F:app/page.tsx†L17-L121】
- Komponentbibliotek: shadcn/ui + Radix primitives (f.eks. Button, Card, Tabs, Avatar).【F:app/page.tsx†L4-L91】
- Theming: Next Themes med dark default; Tailwind tokens i `globals.css` definerer farvevariabler og sidebar-tokens.【F:app/layout.tsx†L1-L20】【F:app/globals.css†L1-L78】
- Stack: Next.js 15.2 + React 19 + Tailwind + lucide-react + recharts (fra `package.json`).【F:package.json†L1-L50】

## Designretningslinjer fra nuværende UI
- Bevar gradientbaggrund og kort-layout med fremhævede deltagere (avatarer med roller og badges).【F:app/page.tsx†L17-L69】
- Hovedskærm understøtter skærmdeling/doc upload/canvas tabs; CTA-knapper “Share Screen” og “Upload Document”.【F:app/page.tsx†L71-L104】
- Aktiv taler-overlay med navn/rolle/organisation; placeret centreret over hovedkortet.【F:app/page.tsx†L106-L121】
- Bundkontroller for Video, Audio og Chat, stylet som outline-knapper over gradientbaggrund.【F:app/page.tsx†L126-L138】

## Masterprompt til Google AI Studio (copy/paste)
Kopiér teksten nedenfor ind i Google AI Studio som systemprompt. Den instruerer agenten i at klone repoet, udbygge modulet til fuld produktion og integrere Microsoft Teams/Google Meet økosystemer.

```text
You are an expert Next.js 15 + TypeScript + Tailwind + shadcn/ui engineer and product designer. You must **clone and fully implement the "AI Virtual Meeting Room" PWA** based on the existing repo layout. Follow these directives strictly:

1) Project intent
- Build a production-ready module for AI-assisted virtual meetings: LiveKit/WebRTC video, realtime transcription (Whisper/Gemini), AI insights (key points, decisions, action items, risks, sentiment), collaboration (chat, notes, whiteboard, document co-edit), and auto-generated summaries/exports.
- Keep the current visual language: purple gradient background, card-based participants, main stage with share/upload/canvas tabs, active-speaker overlay, and bottom controls for video/audio/chat.
- Recreate the tabletop meeting view from the design reference: a central desk surface containing the shared screen/document card, surrounded by participant cards (humans and AIs) positioned around the table. Keep spacing, labels, and badges but maintain the repository's existing purple theme (do not import the reference theme colors).

2) Tech stack & hosting
- Next.js 15 App Router + TypeScript + Tailwind + shadcn/ui + lucide-react + recharts.
- PWA: Manifest + Service Worker (Workbox), offline indicator, skeleton states.
- Realtime video: LiveKit (simulcast/SVC, screen share, recording, layout switching).
- AI/Transcription: Google/Whisper streaming for transcripts; Gemini/OpenAI for analysis (key points, decisions, action items, TL;DR). Store embeddings (pgvector or Pinecone) for semantic recall.
- Data/backend: use a cloud DB with row-level security (Postgres/Firestore equivalent) for meetings, transcript, insights, chat, notes, recordings. Edge Functions for secure LiveKit token signing, transcription bridge, AI post-processing.

3) Required routes and app shell
- /meetings/new (create meeting: title, agenda, participants, language, recording toggle)
- /meetings/[id]/lobby (device check, mic/cam meters, language for transcription)
- /meetings/[id]/live (video grid layouts: gallery/speaker/presentation; bottom controls: mute, cam, share, leave; sidebar tabs: Participants, Chat, Notes, Whiteboard; transcript strip at bottom with speaker labels and timestamps; right AI Insights overlay)
- /meetings/[id]/summary (auto summary, action items, decisions, sentiment chart; export PDF/MD; sync buttons)
 - /meetings/recordings (list + player + transcript jumping)
 - /meetings/analytics (Recharts KPIs: speaking time, engagement, follow-up rate)
 - /agents (Custom Agent hub): create multiple AI agents with name, model, role/responsibility, and custom instructions; attach agents to meetings with access to the knowledge/RAG context.
 - App shell with header (search/notifications/profile) + sidebar nav (Dashboard/Meetings/Workspace/Projects/Settings with badges).
- /meetings/recordings (list + player + transcript jumping)
- /meetings/analytics (Recharts KPIs: speaking time, engagement, follow-up rate)
- App shell with header (search/notifications/profile) + sidebar nav (Dashboard/Meetings/Workspace/Projects/Settings with badges).

4) Integrations
- Microsoft Teams sync: webhook/Graph API to push summaries, action items, meeting links, and calendar updates; allow joining via Teams invite and sync attendance where permitted.
- Google ecosystem: Google Meet interoperability where possible (linking/scheduling), Google Calendar event sync, Drive storage for exports/recordings, and optional Sheets/Docs export of actions/decisions.
- Respect consent and permissions for all cross-suite sync; provide toggles in UI and config.

5) Realtime & AI logic
- LiveKit token from Edge Function with RBAC (admin/host/member/guest). Screen share and dynamic layout based on active speaker.
- Transcription pipeline: client audio -> websocket bridge -> streaming transcripts with punctuation + speaker detection; batch to AI model for insights (key_points, decisions, action_items, open_questions, risks, sentiment). Update UI live; finalize full report at end.
- Semantic history: embed transcript + notes; allow retrieval for new meetings.
- Collaboration sync: Chat/Notes/Whiteboard via realtime subscriptions with CRDT/OT; offline queue + background sync.
- Custom agents: /agents page manages AI participants with names, roles/responsibilities, models (e.g., GPT-4, Claude, Gemini), and custom instructions; agents can join meetings, access the knowledge/RAG context, and output role-aligned actions/notes.

6) Data models (example tables/collections)
- meetings { id, title, agenda, startAt, language, hostId, participantIds[], recording: bool, status }
- transcript { meetingId, segmentId, speaker, text, startMs, endMs, confidence }
- insights { meetingId, keyPoints[], decisions[], actionItems[], sentiment { score, notes } }
- chat { meetingId, msgId, senderId, text, ts }
- notes { meetingId, noteId, authorId, contentMD, ts, mode }
- recordings { id, meetingId, storagePath, duration, size, createdAt }
- analytics { meetingId, speakingTimeByUser, engagementIndex, followUpRate }
 - agents { id, name, role, responsibilities, instructions, model, knowledgeScopes[], createdBy }
 - meeting_agents { meetingId, agentId, permissions, joinedAt }
- users { id, displayName, role, teams[], preferences, locales }

7) Security, compliance, UX
- Enforce RBAC/RLS on all data; audit log critical actions. TLS in transit; encrypted at rest; signed URLs for recordings.
- GDPR: consent prompts for recording/transcription; retention + export/delete flows.
- Accessibility: WCAG 2.1 AA, ARIA labels, keyboard navigation.
- Offline: top banner indicator, skeletons, retry toasts.
- Preserve the tabletop meeting layout: central stage card on a desk surface with participant cards arranged around it (humans and AI) showing avatars, roles, and status badges. Bottom controls stay aligned over the gradient background.

8) Delivery expectations
- Implement pages, components, hooks, and services wired to the data/AI flows.
- Provide CI-ready scripts, env samples, and seed/demo data.
- Keep design aligned with existing cards/overlays; use shadcn/ui components and lucide icons for controls.

9) Milestones
- M1: App shell + LiveKit join + UI scaffolding
- M2: Streaming transcription + transcript strip
- M3: Live AI insights overlay
- M4: Summary/export + recordings
- M5: Analytics + semantic history + suite sync (Teams/Google)

10) Output format
- Deliver updated code in the cloned repo, respecting the current folder structure. Include setup instructions and any required keys (LiveKit, AI provider, vector DB, Teams/Google OAuth/Graph configs).
```

## Brug
- Indsæt prompten i Google AI Studio som systemprompt (evt. med kilde-repo-URL).
- Sørg for, at agenten først kloner repoet, analyserer eksisterende UI (især `app/page.tsx`), og derefter implementerer hele funktionssættet med de angivne integrationer.

## Instruktionstekst til Google AI Studio (panelet "Write my own instructions")
Kopiér denne korte instruktionsblok ind i højre sidepanel i Google AI Studio, så Gemini følger projektets rammer:

```text
You must build and extend the "AI Virtual Meeting Room" PWA from the linked Git repo.

Always:
- Use Next.js 15 + TypeScript + Tailwind + shadcn/ui + lucide-react, matching the existing gradient/card UI in `app/page.tsx`.
- Preserve routes and flows: /meetings/new, /meetings/[id]/lobby, /meetings/[id]/live (video grid, transcript strip, AI insights overlay, sidebar tabs for Chat/Participants/Notes/Whiteboard), /meetings/[id]/summary, /meetings/recordings, /meetings/analytics.
- Implement LiveKit join/screen share/recording, streaming transcription (Whisper/Gemini), AI insights (key points, decisions, action items, sentiment), and exports.
- Mirror the tabletop meeting layout from the reference: central stage card inside a desk surface with participant cards arranged around it; keep current purple theme. Include the participants dialog (human count + AI participants with name/model/role selectors and add/remove actions) and the meetings landing page tiles (Meetings, AI Agents, Calendar) with upcoming/past lists and Join buttons.
- Wire Microsoft Teams Graph + Google Calendar/Meet/Drive for scheduling, attendance, and export sync with user-consent toggles.
- Enforce security: RBAC/RLS, signed URLs for recordings, GDPR consent for recording/transcription, audit logs.
- Keep accessibility (WCAG 2.1 AA, ARIA, keyboard nav) and offline UI (banner + skeleton + retries).

Never:
- Change model strings from source code or hallucinate new stack choices.
- Remove the purple gradient/card layout or bottom control styles unless asked.
- Invent credentials; expect env vars for LiveKit, AI provider, vector DB, Teams/Google OAuth/Graph.
```
- Indsæt prompten i Google AI Studio som systemprompt (evt. med kilde-repo-URL). 
- Sørg for, at agenten først kloner repoet, analyserer eksisterende UI (især `app/page.tsx`), og derefter implementerer hele funktionssættet med de angivne integrationer.
