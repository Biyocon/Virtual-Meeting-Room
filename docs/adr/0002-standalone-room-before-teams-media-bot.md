---
status: accepted
---

# Standalone tabletop-rum før Teams media-bot

Vi skulle afgøre, om MVP'en bærer sin egen real-time media eller bygges som en Teams in-meeting app oven på Teams' media. **Beslutning:** MVP'en bygges som et **standalone tabletop-rum med egen real-time media (LiveKit/WebRTC)** på Biyocon; Microsoft Teams bliver en fase 2-5 integrationskanal, ikke MVP'ens media-host. **Hvorfor:** det viser produktets differentiering (tabletop-rum + digitale medarbejdere) hurtigst og uden Teams-platformens tungeste, mest gated del (real-time media-bot), som ellers ville blokere før kernen er bevist.

## Considered Options

- **(A) Standalone tabletop-rum med egen media** (valgt).
- **(B) Teams in-meeting app først** (fravalgt som MVP) — Teams bærer media, men agent-tale ind i mødet kræver en media-bot (Graph real-time media permissions, compliance) → udskudt til fase 4.

## Consequences

**MVP in-scope:**
- tabletop-rum set oppefra
- menneskelige deltagere som pladser/video/tilstedeværelse
- 1-3 digitale medarbejdere som avatar-pladser
- aktiv-taler-state
- agentrespons via tekst først, derefter TTS
- videnscope pr. møde
- mødechat/transskription som intern datakilde
- LiveKit/WebRTC som møde-media-lag

**MVP out-of-scope (eksplicitte no-s):**
- injektion af AI-medarbejdere i et live Teams-møde
- tale som Teams media-bot
- Graph real-time media permissions
- fuld Microsoft 365 enterprise-compliance i første demo
- avanceret lip-sync, 3D-avatar eller fuld voice cloning

**Teams-rækkefølge** (detaljeret roadmap i Stage 3):
1. Standalone tabletop MVP
2. Teams sidepanel/meeting tab — agentstyring, projektvalg, beslutningslog/action items
3. Teams bot/notifikation uden media
4. Teams real-time media-bot — agenter taler direkte ind i et kørende Teams-møde
5. Enterprise M365 — Entra ID, Graph, SharePoint/OneDrive scopes, audit logs, tenant isolation

Teams SDK/Graph/meeting-extensions designes fra start som fremtidig integrationsflade, men real-time media-bot udskydes.
