# Agent Sidecar (M2+)

Python/FastAPI sidecar behind the Agent Event Contract (lib/agent/contract.ts).

## Setup

```bash
cd sidecar
python -m pip install -e .
```

## Development

```bash
python -m uvicorn src.agent_sidecar.main:app --reload --port 8000
```

Then set `NEXT_PUBLIC_AGENT_SIDECAR_URL=http://localhost:8000` in `.env.local` to activate M2 over M0 stub.

## Scope (M2)

Stub implementation only:
- `/health` liveness check
- `POST /agent/respond` accepts commands (no-op, echoes back 202)
- `GET /agent/events/{meeting_id}` SSE stream with synthetic event sequence

No real model, TTS/STT, RAG, or Council/Compare yet.

## TODO (post-M2)

- [ ] Integrate real model (OpenAI, Anthropic, etc.)
- [ ] Add TTS (Azure/ElevenLabs)
- [ ] Add STT (Azure Whisper)
- [ ] Add RAG backend
- [ ] Council & Compare capabilities
