---
status: accepted
---

# Cloud TTS med Azure Neural TTS til MVP; ElevenLabs/self-host som senere spor

Vi skulle vælge TTS-strategi til MVP'ens standardstemmer. **Beslutning:** MVP bruger **cloud TTS med standardstemmer i en EU-region**, og **Azure Neural TTS** som default-provider, fordi produktets langsigtede platform er Microsoft Teams/M365/Entra/Graph, og Azure Speech ligger nærmest den retning. **ElevenLabs** holdes som senere premium-/voice-cloning-spor. **Self-hosted TTS** (odysseus: Piper/Coqui/XTTS, eller Azure Speech-containere) designes som enterprise-exit, men er ikke MVP-krav. STT er separat afgjort: **Whisper** (codebase-grounded i `iqra`/`odysseus`).

## Considered Options

- **Azure Neural TTS** (valgt til MVP) — M365/Entra-nærhed; residency indbygget i ressourcens region (ingen ekstra tier); container/edge-exit muligt.
- **ElevenLabs** (fravalgt som MVP-default, valgt som senere spor) — stærk stemmekvalitet + kloning, men data residency er en Enterprise-feature med isolerede miljøer → mindre oplagt som hurtig-demo-default.
- **Self-hosted (odysseus-sporet)** (fravalgt som MVP-krav, valgt som exit) — fuld kontrol, men GPU/inferens-drift og typisk lavere kvalitet/streaming i MVP.

## Consequences

- **Adapter-baseret provider** (`azure | elevenlabs | self_hosted`), så provideren kan skiftes uden at ændre agentmodellen — samme Cloud→self-host-portabilitetsregel som media (ADR-0003).
- **Stemmeprofil pr. digital medarbejder** bærer mindst: `voiceProvider`, `voiceId`, `language`, `style`, `speakingRate`, `pitch`, `consentStatus`, `syntheticVoiceDisclosure`. (Formel `AgentVoiceProfile`-type defineres i Stage 2-datamodellen.)
- **`consentStatus = standard_voice`** i MVP. **`cloned_voice` er ikke tilladt i MVP** → genintroduceres via egen samtykke-gated ADR (kan læne sig på Azure Custom/Personal Voice's indbyggede samtykke-/godkendelsesflow).
- **Syntetisk-stemme-disclosure er obligatorisk i UI'et**, fx "Digital medarbejder · syntetisk stemme".
- **Agentens outputtekst sendes til TTS-provideren** → MVP kun med testdata/lavrisiko data (konsistent med ADR-0003); brug EU-region/-endpoint.
- **Retention fra start:** TTS-logs, audio-cache og genereret tale skal have eksplicitte retention-/sletteregler.

## Kilder

- Azure Speech — supported regions / residency (data forbliver i ressourcens region): https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions
- Azure Speech — container/edge on-prem: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview
- Azure Speech — data/privacy for TTS + Custom/Personal Voice samtykkeflow: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security
- ElevenLabs — data residency (Enterprise): https://elevenlabs.io/docs/overview/administration/data-residency
