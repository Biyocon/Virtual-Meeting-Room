# Avatar Style Spec (MVP)

Letvægts-designguide for digitale medarbejderes avatarer i MVP. **Ikke en ADR** — let at reversere; dette fryser kun art direction, ikke arkitektur.

## Beslutning

MVP bruger et **nygenereret, ensartet portræt-sæt** i illustreret/stiliseret stil. `custom/Avatar/` bruges **kun** som intern fallback: klikprototyper, tidlige UI-tests, eller når et agentkort endnu mangler et nyt portræt.

Fidelitet er låst af ADR-0002: 2D, statisk portræt + speaking-state. **Ingen** lip-sync, 3D eller fotorealistiske talking heads i MVP (det ligger i samme senere fase som voice cloning).

## Style-regler for portræt-sættet

- Stil: illustreret / semi-flat / moderne produktillustration — **ikke fotorealistisk**
- Samme framing: bryst/ansigt, frontalt eller let 3/4-vendt
- Samme baggrundslogik: neutral eller let farvekodet
- Samme lys og kontrast
- Samme billedformat (fx 1:1)
- Rolle-system: farveaccent eller badge pr. rolle
- Tydelig forskel mellem agenter, men samme overordnede stilfamilie

## Per-agent felter (MVP)

`avatarImage` · `avatarStyle = illustrated` · `roleLabel` · `status = idle | listening | thinking | speaking` · `speakerRing` · `waveform` · `agentLabel` · evt. `colorAccent`

Begrundelse: visuel sammenhæng gør "pladsen ved bordet" produktagtig og læsbar; illustreret stil reducerer uncanny valley og gør digitale medarbejdere tydeligt identificerbare som syntetiske aktører.
