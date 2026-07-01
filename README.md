# Virtual Meeting Room (VMR)

AI-drevet virtuelt møderum hvor "digitale medarbejdere" — AI-agenter med syntetisk stemme — sidder ved bordet som ligestillede, tydeligt mærkede deltagere. Agenter lytter (Whisper STT), taler (Azure Neural TTS), citerer kilder (KnowledgeScope RAG) og bærer altid et synligt "Syntetisk stemme"-badge.

> **Status:** Under udvikling — milestone M2 (Python-sidecar v0). Se `docs/KØREPLAN.md` for aktuel status og `primer.md` for seneste session-kondensat.

## Arkitektur

- **UI/BFF:** Next.js 15 (App Router) + React 19 + TypeScript · Tailwind v4 + shadcn/ui
- **Agent-runtime:** Python FastAPI sidecar (LLM, TTS/STT-adaptere, RAG) — ADR-0005
- **Kontrakt:** `AgentEvent`/`AgentCommand` — Zod (TS) ↔ Pydantic (Python) ↔ `agent-event.schema.json`, drift-guarded
- **Media (planlagt M6):** LiveKit Cloud EU · **TTS/STT (M3/M4):** Azure Neural TTS + Whisper, EU-residency

Alle arkitekturbeslutninger er dokumenteret som ADR'er i `docs/adr/`.

## Kom i gang

```bash
pnpm install
pnpm dev                    # → http://localhost:3000/agent-demo (fungerende demo)
pnpm test:contract          # kontrakt-drift-guard

# Sidecar (Python 3.11+)
cd sidecar
pip install -e ".[dev]"
python -m uvicorn agent_sidecar.main:app --reload --port 8000
pytest tests/
```

Demoen på `/agent-demo` kører mod TS-stub som default. Sæt `NEXT_PUBLIC_AGENT_SIDECAR_URL=http://localhost:8000` for sidecar-mode (OBS: end-to-end-kobling færdiggøres i M2 — se `docs/active/`).

## Dokumentation

| Dokument | Indhold |
|----------|---------|
| `docs/PRD.md` | Krav, personas, P0–P2 features, successmetrikker |
| `docs/KØREPLAN.md` | Milestones M0–M9 med status og gates |
| `docs/DEPS.md` | Afhængigheder, kritisk sti, change-impact-procedure |
| `docs/active/` | Aktive tickets med acceptkriterier |
| `docs/adr/` | Arkitekturbeslutninger (immutable) |
| `docs/architecture/` | Stage-2-arkitektur + stage-3-eksekveringsplan |
| `CLAUDE.md` | Instruktioner til AI-agenter der arbejder i repoet |

## Principper

- **Disclosure-first:** AI-status er altid synlig — badge kan ikke slås fra (ADR-0004)
- **Kontrakt-first:** UI kender kun `AgentRuntime`-interfacet; runtime er swappable (ADR-0005)
- **EU-residency:** LiveKit EU + Azure EU; testdata indtil videre (ADR-0003)
- **Audit-alt:** Alle agent-handlinger producerer `audit.event`

## Licens

Ikke fastlagt endnu (se ADR-0001 — afklares før distribution).
