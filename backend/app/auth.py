"""Lightweight per-plan member auth.

On create/join the server generates a random token, returns it ONCE, and stores only its
hash. The frontend sends it back as `Authorization: Bearer <token>`.
"""

import hashlib
import secrets

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Member, MemberRole


def new_token() -> tuple[str, str]:
    """Returns (raw_token_for_client, hash_for_db)."""
    raw = secrets.token_urlsafe(32)
    return raw, hash_token(raw)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def current_member(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> Member:
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing member token")
    member = db.scalar(select(Member).where(Member.token_hash == hash_token(authorization[7:])))
    if member is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid member token")
    return member


def require_plan_member(plan_id: str, member: Member) -> None:
    if member.plan_id != plan_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You are not in this plan")


def require_organizer(plan_id: str, member: Member) -> None:
    require_plan_member(plan_id, member)
    if member.role != MemberRole.organizer:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the organizer can do this")
