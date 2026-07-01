---
id: "#6"
title: "AgentProfile-loader + sidecar-struktur pr. stage-3 §5"
milestone: "M2"
status: active
prioritet: "P1"
deps:
  - "#1"
blocks:
  - "M3-1"
  - "M4-1"
  - "M5-1"
oprettet: "2026-07-01"
sidst_opdateret: "2026-07-01"
---

## Hvad & Hvorfor

Sidecaren er én 366-linjers `main.py`. Stage-3 §5 definerer strukturen (`routes/`, `contracts.py`, `runtime/profile_loader.py`, `runtime/instance.py`, `policy.py`, `audit.py`, `adapters/`) som M3–M5 bygger ovenpå. AgentProfile-loaderen (custom-format) er M2-leverance: agenter skal defineres som konfiguration, ikke kode.

## Done ser sådan ud

`sidecar/profiles/*.yaml` definerer 3+ agenter (navn, rolle, colorAccent, voiceProfile-stub, knowledgeScope-stub). Sidecar loader dem ved opstart; ugyldig profil giver klar fejl. `MeetingAgentInstance` oprettes ved møde-start, lukkes ved møde-slut, alt auditeret.

## Teknisk scope

- [ ] Split `main.py` → `contracts.py`, `routes/agent.py`, `runtime/profile_loader.py`, `runtime/instance.py`, `audit.py` (adapters/ venter til M3/M4)
- [ ] Pydantic `AgentProfile`-model + YAML-loader med validering
- [ ] 3 eksempel-profiler (matcher demo: PM, analytiker, facilitator)
- [ ] `MeetingAgentInstance`-livscyklus med owner-scope + `audit.event` ved create/close
- [ ] Pydantic v2-style `model_config = ConfigDict(extra="forbid")` overalt (også payloads — udvid drift-guard)
- [ ] Opdatér `sidecar/README.md` run-kommando (installeret pakke, ikke sys.path-hack)

## Relevante filer

- `sidecar/src/agent_sidecar/main.py`
- `docs/architecture/stage-3-build-execution-plan.md` §5 (mål-struktur)
- `lib/agent/contract.ts` (`MeetingAgentInstance`-type som facit)
- `sidecar/tests/` (opdatér imports til installeret pakke)

## Acceptkriterie

- [ ] 3+ profiler loader uden fejl; bevidst ugyldig profil → klar fejlbesked, ikke traceback
- [ ] Struktur matcher stage-3 §5 (minus adapters)
- [ ] Alle events fra instance bærer `tenantId + meetingId + agentInstanceId`
- [ ] pytest grøn; ingen `sys.path.insert` i tests

## Blocker / noter

2026-07-01: Kør EFTER #1 er merget — split af main.py samtidig med #1's buskobling giver konflikthelvede.
