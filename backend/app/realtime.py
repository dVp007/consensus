"""In-memory WebSocket hub: one 'room' per plan.

Events are small JSON messages telling clients what changed, e.g.
  {"type": "member_joined", "member": {...}}
  {"type": "interview_done", "member_id": "..."}
  {"type": "status_changed", "status": "voting"}
  {"type": "agent_step", "step": "Checking 5 members' budgets"}
  {"type": "vote_cast", "proposal_id": "..."}

Clients then refetch what they need. NEVER broadcast private data (messages, constraints).

Limitation: in-memory means one server process only. Stretch goal: Redis pub/sub so you can
run multiple workers (great interview talking point).
"""

from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, plan_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self.rooms[plan_id].add(ws)

    def disconnect(self, plan_id: str, ws: WebSocket) -> None:
        self.rooms[plan_id].discard(ws)

    async def broadcast(self, plan_id: str, event: dict) -> None:
        dead = []
        for ws in self.rooms[plan_id]:
            try:
                await ws.send_json(event)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(plan_id, ws)


manager = ConnectionManager()
