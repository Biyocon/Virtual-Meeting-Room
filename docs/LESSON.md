# Lessons Learned: Virtual Meeting Room (VMR)

<!--
HVORNÅR SKRIVES EN LESSON:
  - Ved afslutning af en MILESTONE (ikke en ticket — for meget noise)
  - Ved en post-mortem efter en alvorlig fejl/bloker
  - Aldrig under en aktiv sprint (refleksion kræver distance)

FORMÅL:
  Forhindre gentagelse af fejl. "Hvad ændrer vi fremover" SKAL have en handling.
-->

---

## M0 + M1 — Contract & Agent-kort — Afsluttet (commit `93d60f1`, PR #4)

**Sprints:** M0-kontrakt → M1-demo
**Tests ved start → slut:** 0 → contract-test (TS) + 2 pytest-moduler (sidecar)

---

### Hvad gik godt

- Kontrakt-first-tilgangen (Zod + JSON-schema-spejl + drift-test) gjorde swap-seamet (`sidecarClient.ts`) rent — UI kender kun `AgentRuntime`-interfacet
- CorrelationId-dedup i `useAgentEvents.ts` løste reconnect-duplikat-problemet fra testplan §6 inden det opstod i praksis
- Disclosure-badge uden disable-prop (ADR-0004) implementeret som hårdt krav fra dag ét

### Hvad gik skidt

- **Commit-besked "M2: Complete sidecar implementation" overdrev groft** — reelt ~40%: respond- og events-endpoints er ukoblede, BFF proxy'er ikke sidecar-stream, agentInstanceId hardcoded. Kostede en fuld re-audit at opdage
- **Planlægningsdocs driftede fra kode på under en uge**: KØREPLAN sagde "M0 AKTIV" mens git var på M2; milestone-definitioner matchede ikke stage-3-planen de refererede til
- **Stage-3-planen antog Biyocon-assets der ikke findes** (`lib/livekit`, `lib/auth`, `lib/privacy`, `hooks/useMeetingRealtime`, `components/tabletop/`) — M6/M8-estimater bygget på "genbrug" er reelt greenfield
- Drift-guard-testen er overfladisk: sammenligner kun typenavne-sæt, ikke payload-felter på tværs af TS/Python

### Hvad vi ændrer fremover

- **Milestone markeres kun done når DoD-sætningen fra stage-3 §4 kan demonstreres** — ikke når koden "findes". Verifikation via docs/qa/-release-tjek før merge til main (håndhæves fra M2-gate)
- **Docs opdateres i samme PR som koden** — en PR der ændrer milestone-status uden KØREPLAN-opdatering afvises (regel #3 i tasks/lessons.md)
- **Antagelser om eksisterende assets verificeres med Glob/ls før estimering** — aldrig fra dokumentation alene
- **CI (ticket #4) prioriteres som isoleret task NU** så drift-guard + pytest kører automatisk; payload-dyb validering tilføjes i #6

### Estimat vs. faktisk

| Sprint | Estimeret | Faktisk | Delta | Årsag til afvigelse |
|--------|-----------|---------|-------|---------------------|
| M0 | 1 uge | ~1 uge | ±0 | Kontrakt-scope var velafgrænset |
| M1 | 1 uge | ~1 uge (demo-scope) | ±0 | Tabletop-integration blev (rigtigt) udskudt |
| M2 | 1 uge | ⏳ >1 uge | + | DoD-krav (kobling+proxy) undervurderet |

---

### Næste lesson skrives ved

Afslutning af M2 — Sidecar v0 (DoD: swap uden UI-ændring demonstreret)
