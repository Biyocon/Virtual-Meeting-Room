# Agent Sidecar (M2+)

Python/FastAPI sidecar behind the Agent Event Contract (`lib/agent/contract.ts`).

## Setup

Install the sidecar as a package (required for correct imports):

```bash
cd sidecar
python -m pip install -e .
```

## Development

Run from the installed package:

```bash
cd sidecar
python -m uvicorn agent_sidecar.main:app --reload --port 8000
```

Then set `AGENT_SIDECAR_URL=http://localhost:8000` in the Next.js app's `.env.local`
to activate M2 sidecar mode instead of the M0 TS stub.

## Scope (M2)

Stub implementation only:

- `/health` liveness check
- `POST /agent/respond` accepts commands and returns 202
- `GET /agent/events/{meeting_id}` SSE stream with synthetic event sequence
- `sidecar/profiles/*.yaml` loaded at startup; `agent.add` creates a
  `MeetingAgentInstance`
- Owner-scoping (`x-tenant-id`) enforced on both endpoints

No real model, TTS/STT, RAG, or Council/Compare yet.

## Project layout

```
src/agent_sidecar/
  main.py            FastAPI app + lifespan
  contracts.py       Pydantic mirror of AgentEvent/AgentCommand
  audit.py           audit.event helpers
  routes/agent.py    HTTP endpoints
  runtime/
    state.py         MeetingBus + tenant registry (dev seam)
    profile_loader.py  AgentProfile YAML loader
    instance.py      MeetingAgentInstance lifecycle
profiles/*.yaml      Static agent persona definitions
tests/               pytest suite (no sys.path hacks)
```

## TODO (post-M2)

- [ ] Integrate real model (OpenAI, Anthropic, etc.)
- [ ] Add TTS (Azure/ElevenLabs)
- [ ] Add STT (Azure Whisper)
- [ ] Add RAG backend
- [ ] Council & Compare capabilities
