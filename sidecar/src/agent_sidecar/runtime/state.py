"""Shared in-process runtime state.

Dev-only seam mirroring lib/agent/bus.ts. Swap point for Redis/NATS when the
sidecar goes multi-process (post-M2).
"""

import asyncio
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_sidecar.contracts import AgentEvent


HEARTBEAT_SECONDS = 15.0
DELTA_DELAY_SECONDS = 0.15


class MeetingBus:
    """Per-meeting fan-out of AgentEvents to SSE subscribers."""

    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue]] = {}

    def subscribe(self, meeting_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self._subscribers.setdefault(meeting_id, set()).add(queue)
        return queue

    def unsubscribe(self, meeting_id: str, queue: asyncio.Queue) -> None:
        subscribers = self._subscribers.get(meeting_id)
        if subscribers is None:
            return
        subscribers.discard(queue)
        if not subscribers:
            del self._subscribers[meeting_id]

    async def publish(self, meeting_id: str, event: "AgentEvent") -> None:
        for queue in self._subscribers.get(meeting_id, ()):
            queue.put_nowait(event)


# Single process-local bus instance.
bus = MeetingBus()


# ── Owner-scoping (ticket #5) ────────────────────────────────────────────────
# MVP tenant-registry: dev-only, in-memory, process-local (same seam as the bus).
# meetingId -> tenantId, claimed by the first command that touches it.

_tenant_registry: dict[str, str] = {}


class TenantMismatch(Exception):
    def __init__(self, meeting_id: str, expected: str, actual: str) -> None:
        super().__init__(f"meeting {meeting_id} is owned by a different tenant")
        self.meeting_id = meeting_id
        self.expected = expected
        self.actual = actual


def claim_or_check_tenant(meeting_id: str, tenant_id: str) -> None:
    """Used by /agent/respond.

    The first command for a meetingId claims it for that tenant; later commands
    from a different tenantId are rejected.
    """
    existing = _tenant_registry.get(meeting_id)
    if existing is None:
        _tenant_registry[meeting_id] = tenant_id
        return
    if existing != tenant_id:
        raise TenantMismatch(meeting_id, existing, tenant_id)


def check_tenant_readonly(meeting_id: str, tenant_id: str) -> None:
    """Used by /agent/events.

    Never claims ownership — subscribing must not be able to squat a meetingId
    before its owner's first command claims it. Unclaimed meetings have nothing
    to leak, so any tenant may open the stream; it will simply see no events
    until the owner acts.
    """
    existing = _tenant_registry.get(meeting_id)
    if existing is not None and existing != tenant_id:
        raise TenantMismatch(meeting_id, existing, tenant_id)


def reset_tenant_registry() -> None:
    """Test-only: reset between test cases."""
    _tenant_registry.clear()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
