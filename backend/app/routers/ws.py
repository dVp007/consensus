from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.auth import hash_token
from app.db import SessionLocal
from app.models import Member
from app.realtime import manager

router = APIRouter()


@router.websocket("/ws/plans/{plan_id}")
async def plan_events(ws: WebSocket, plan_id: str, token: str = ""):
    """Browsers can't set headers on WebSockets, so the token comes as ?token=..."""
    with SessionLocal() as db:
        member = db.query(Member).filter(Member.token_hash == hash_token(token)).first()
    if member is None or member.plan_id != plan_id:
        await ws.close(code=4401)
        return

    await manager.connect(plan_id, ws)
    try:
        while True:
            await ws.receive_text()  # keep-alive; clients don't need to send anything
    except WebSocketDisconnect:
        manager.disconnect(plan_id, ws)
