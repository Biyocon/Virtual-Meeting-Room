"""Agent event contract sidecar: Python/FastAPI application entrypoint (M2).

Mirrors lib/agent/contract.ts (TS source of truth). Validates all inputs/outputs
against the contract. No real model/TTS/STT/RAG yet (M3+).
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from agent_sidecar.routes.agent import router as agent_router
from agent_sidecar.runtime.profile_loader import get_profiles


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown logic."""
    print("[sidecar] Booting agent sidecar (Python/FastAPI M2)")
    # Load profiles eagerly so startup fails fast on invalid configuration.
    profiles = get_profiles()
    print(f"[sidecar] Loaded {len(profiles)} agent profiles")
    # TODO M3+: Initialize model, TTS/STT, runtime
    yield
    print("[sidecar] Shutdown")


app = FastAPI(title="Agent Sidecar", lifespan=lifespan)
app.include_router(agent_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
