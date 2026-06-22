---
status: accepted
---

# LiveKit Cloud til MVP, self-host som enterprise-exit

Vi skulle vælge deployment-model for LiveKit (biblioteket selv er afgjort af codebase-evidens: Biyocon wirer allerede LiveKit, Apache-2.0). **Beslutning:** MVP-media kører på **LiveKit Cloud** (Build/Ship-tier, kun testdata); **self-hosted LiveKit** designes som eksplicit exit-path for enterprise/følsomme data/streng data-residency, ikke som MVP-krav. **Arkitekturregel:** LiveKit-endpoint, token-server og media-deployment skal kunne skiftes uden omskrivning af frontend/room-model.

## Considered Options

- **LiveKit Cloud** (valgt til MVP) — hurtigst, ingen SFU-drift; portabelt til self-host senere (samme komponenter/API/SDK, kun endpoint skifter).
- **LiveKit self-hosted** (fravalgt som MVP-krav, valgt som enterprise-exit) — fuld kontrol + EU/DK-residency, men du driver services + load balancer/TLS/TURN/Redis + monitoring/patching/on-call selv.

## Consequences

- **Portabilitet:** Cloud↔self-host er ikke en one-way door — applikationskoden er portabel, kun connection-endpoint ændres.
- **GDPR-residency på Cloud koster og kræver opsætning:** region pinning fås kun på **Scale-tier ($500/md) og op**, skal **anmodes via LiveKit Support**, og **slår automatisk failover fra**. På Build/Ship-tier kan media route uden for EU.
- **Observability-data → USA:** transcripts, traces, logs og audio-recordings behandles/lagres i USA (pr. feb. 2026) uanset media-region; skal **slås fra på projektniveau** ved residency-krav.
- **Model-API'er routes uafhængigt:** STT/TTS/LLM kan behandle data uden for regionen selv med media-pinning — brug EU-endpoints (fx `api.eu.deepgram.com`, `eu.api.openai.com`, `api.eu.residency.elevenlabs.io`) hvis residency kræves.
- **MVP-compliance-scope (eksplicitte no-s):** kun testdata/lavrisiko interne data. **Ingen** rigtige kundedata, optagelser, fuld transskription, følsomme dokumenter eller personoplysninger, før DPA, retention, logging, region og dataflow er lukket. Med følsomme data fra start: self-host eller isolér dem uden for Cloud-MVP'en.

## Kilder

- LiveKit — Cloud vs self-host (portabilitet): https://livekit.com/blog/livekit-cloud-vs-self-host
- LiveKit — Region pinning (Support-anmodning, failover): https://docs.livekit.io/deploy/admin/regions/region-pinning/
- LiveKit — Checklist for regional deployments (observability i USA, model-endpoints): https://livekit.com/blog/checklist-for-regional-deployments
- LiveKit — pricing (residency = Scale-tier): https://livekit.com (Pricing)
