# Plan: M2 Sidecar v0 — swap uden UI-ændring
**Oprettet:** 2026-07-01
**Ref:** `docs/active/#1` `#2` `#3` | `docs/PRD.md §4 P0` | `docs/architecture/stage-3-build-execution-plan.md` §4–§5
**Status:** IMPLEMENTERET (trin 1–6, 2026-07-09) — kun M2-gate udestår

<!--
Skrives ÉN GANG, læses FØR implementering starter.
Opdateres IKKE under implementering — brug task-tickets til løbende noter.
-->

---

## Problem der løses

M2-DoD: "TS-stub byttes til Python-sidecar uden UI-ændring." Tre konkrete brud i dag:

1. Sidecar: `/agent/respond` discarder kommandoen; SSE afspiller canned sekvens uafhængigt af kommandoer
2. BFF: events-routen lytter kun på lokal bus — sidecar-events når aldrig UI'et
3. IDs: sidecar hardcoder `agent-0`; UI filtrerer på ægte instanceId → alt filtreres væk

Konsekvens: nuværende `.env.local`-konfiguration (sidecar aktiveret) er brudt end-to-end.

---

## Løsningsdesign

### Tilgang

Spejl BFF'ens bus-arkitektur i sidecaren: en meeting-scoped asyncio-bus hvor `/agent/respond` publicerer og SSE-generatoren subscriber. BFF'ens events-route bliver en betinget proxy: sidecar-URL sat → pipe sidecar-SSE igennem (merged med BFF'ens egne audit-events); ellers lokal bus som i dag. UI-laget (`useAgentEvents`, `AgentCard`) røres IKKE — det er selve DoD-testen.

### Alternativer overvejet

| Alternativ | Fordele | Ulemper | Afvist fordi |
|------------|---------|---------|--------------|
| UI kobler direkte på sidecar-SSE | Simplere BFF | Bryder BFF-arkitekturen (ADR-0005: TS BFF ejer streaming/auth); CORS; scoping umulig i M8 | ADR-0005-brud |
| WebSocket i stedet for SSE | Bidirektionel | Kontrakt + UI allerede SSE; ingen behov for bidirektionel endnu | Unødig scope-udvidelse |
| Redis/NATS som bus nu | Multi-process klar | Overkill for M2; in-memory er dokumenteret dev-seam | YAGNI — swap-punkt findes allerede |

---

## Datamodel / API-kontrakt

Ingen kontraktændringer. Eksisterende `AgentEvent`/`AgentCommand` fra `lib/agent/agent-event.schema.json` bruges uændret — det er pointen.

Sidecar-internt (nyt, ikke kontrakt):

```python
class MeetingBus:
    """Per-meeting asyncio fan-out. Dev-only seam, spejler lib/agent/bus.ts."""
    def subscribe(self, meeting_id: str) -> AsyncIterator[AgentEventModel]: ...
    async def publish(self, meeting_id: str, event: AgentEventModel) -> None: ...
```

---

## Berørte filer

| Fil | Ændring | Note |
|-----|---------|------|
| `sidecar/src/agent_sidecar/main.py` | MODIFICER | + MeetingBus, respond→publish, SSE→subscribe, heartbeat, ID-passthrough |
| `sidecar/tests/test_endpoints.py` | MODIFICER | Kobling-, reconnect-, ID-tests |
| `app/api/agent/events/[meetingId]/route.ts` | MODIFICER | Betinget sidecar-proxy + enqueue-guard |
| `app/api/agent/respond/route.ts` | INGEN (verificér) | Videresender allerede via sidecarClient |
| `hooks/useAgentEvents.ts`, `components/agent-card.tsx` | INGEN | DoD: diff skal være tom |
| `.github/workflows/ci.yml` | TILFØJ (#4) | Parallelt spor |

---

## Rækkefølge for implementering

1. **#1** Sidecar-bus + kobling (pytest-drevet, ingen TS-ændringer)
2. **#4** CI parallelt (uafhængig)
3. **#2** BFF-proxy (nu er der noget ægte at proxy'e)
4. **#3** ID-passthrough + demo-verifikation end-to-end
5. **#5** Owner-scoping (bygger på proxy-laget)
6. **#6** Struktur-split + profile-loader (efter #1 merget — undgå merge-konflikt i main.py)
7. M2-gate: `docs/qa/release-YYYY-MM-DD.md` udfyldes (template: `~/.claude/templates/docs/qa/_RELEASE.md`)

---

## Risici

| Risiko | Sandsynlighed | Konsekvens | Afbødning |
|--------|--------------|------------|-----------|
| SSE-proxy buffering i Next.js (nodejs runtime) | Medium | Events klumper/forsinkes | `runtime="nodejs"` allerede sat; test med curl før UI; flush per event |
| Reconnect-replay giver duplikat-finals | Medium | UI viser dobbelt svar | correlationId-dedup findes i hook; sidecar må ikke replaye finals (test i #1) |
| `tsc --noEmit` i CI afslører skjulte typefejl | Høj | CI rød fra dag ét | Fix i #4 eller trapvis: typecheck non-blocking → blocking i #8 |
| main.py-split (#6) konflikter med #1 | Høj | Merge-helvede | Sekventielt: #6 starter først efter #1 er merget |

---

## Definition of done

- [x] `/agent-demo`-endpoints kører fuld sekvens mod sidecar (curl-E2E); `git diff hooks/ components/` tom
- [x] Stub-mode (uden env-var) uændret
- [x] `pnpm test:contract` + pytest grønne i CI
- [x] Scoping-test: forkert tenantId → 403 (2026-07-09, #5 — se note nedenfor)
- [x] `docs/qa/`-release-tjek udfyldt og GODKENDT (2026-07-09, efter fix af payload.agentInstanceId-bug — se qa/release-2026-07-09.md)

## #6 Struktur-split + AgentProfile-loader — implementeringsnote (2026-07-09)

`main.py` er split ud efter stage-3 §5:
- `contracts.py` — alle Pydantic-modeller inkl. `AgentProfile` og `MeetingAgentInstance`
- `routes/agent.py` — `/health`, `/agent/respond`, `/agent/events/{meeting_id}`
- `runtime/state.py` — `MeetingBus` + tenant registry
- `runtime/profile_loader.py` — YAML-loader til `sidecar/profiles/*.yaml`
- `runtime/instance.py` — `MeetingAgentInstance`-livscyklus
- `audit.py` — `audit.event`/`scope/denied` helpers
- `main.py` — FastAPI app-factory + lifespan, eager profile-loading

Profiler: `pm`, `analyst`, `facilitator` (navn, rolle, accentColor, voiceProfile-stub,
knowledgeScope-stub, skills, systemPrompt, model). Loader fejler hurtigt ved opstart med
klar besked ved ugyldig YAML/duplicate ID/manglende felter.

`AgentCommand`-union er ændret fra manuel `if/elif`-parse til en `_parse_command()`
hjælper; alle Pydantic-modeller bruger nu `model_config = ConfigDict(extra="forbid")`.

Tests: `sys.path.insert` fjernet overalt; imports bruger installeret pakke
(`agent_sidecar.*`). Nye tests: `test_profiles.py` (loader + instance-lifecycle).

Verifikation: 41/41 pytest grønne, `pnpm test:contract` OK, `npx tsc --noEmit` OK.

**QA-fund og fix (2026-07-09):** Uafhængig manuel E2E afslørede, at `agent.respond`
med `scope.agentInstanceId` udeladt/afvigende fra `payload.agentInstanceId` (kontrakt-
lovligt) fik `run_respond_sequence` til at crashe stille med `InstanceNotFound`.
Rodårsag: `agent_respond()` brugte `scope.agentInstanceId` til fallback-instans-opret,
men `run_respond_sequence()` brugte `payload.agentInstanceId`. Fix: payload bruges nu
konsekvent som autoritativ nøgle. Ny regressionstest:
`test_agent_respond_payload_instance_id_without_scope`. Fuld rapport i
`docs/qa/release-2026-07-09.md`.

## #5 Owner-scoping — implementeringsnote (2026-07-09)

Sidecar: `_tenant_registry: dict[meeting_id] -> tenant_id`, `POST /agent/respond`
claimer/tjekker (`_claim_or_check_tenant`), `GET /agent/events/{meeting_id}` kræver
`x-tenant-id`-header og tjekker read-only (`_check_tenant_readonly` — claimer aldrig,
så en subscriber ikke kan "squatte" et meetingId før ejeren har svaret første gang).
Mismatch/manglende header → 403 + `audit.event` (`action=scope/denied`). 26/26 pytest grønne.

BFF: `lib/agent/tenantRegistry.ts` spejler samme claim/check-logik. `respond/route.ts`
tjekker før den kalder runtime; `events/[meetingId]/route.ts` læser `tenantId` som
query-param (EventSource kan ikke sætte custom headers) og sender den videre som
`x-tenant-id` til sidecaren. `useAgentEvents`/`/agent-demo` opdateret til at sende
`tenantId` med.

**Fund undervejs:** et almindeligt modul-niveau `Map` blev nulstillet af Next.js
dev-mode hot-reload/on-demand-kompilering på tværs af routes (verificeret med curl:
`size: 0` fra events-routen, selvom respond-routen lige havde registreret samme
meetingId). Rettet med `globalThis`-backed singleton (samme mønster som fx
Prisma-client-singletons) — kun et dev-mode-fænomen, men værd at vide, hvis `bus.ts`
(samme modul-singleton-mønster, ikke rørt her) nogensinde viser lignende symptomer.

E2E verificeret manuelt (curl, sidecar+Next dev kørende): korrekt tenant → 202/200,
forkert tenant på respond → 403, events uden `tenantId` → 403, events med forkert
`tenantId` → 403 (afvist af BFF FØR sidecar-kald), events på uklaimet meeting → 200
(intet at lække).
