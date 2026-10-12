"""Request/response shapes (Pydantic). Keep these separate from DB models so you never
accidentally leak private fields like token_hash or another member's constraints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ConstraintCategory, MemberRole, PlanStatus


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- plans & members ----------
class PlanCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    organizer_name: str = Field(min_length=1, max_length=80)


class JoinPlan(BaseModel):
    display_name: str = Field(min_length=1, max_length=80)


class MemberPublic(ORM):
    """What OTHER members may see about someone: no constraints, no messages."""

    id: str
    display_name: str
    role: MemberRole
    interview_done: bool


class PlanOut(ORM):
    id: str
    title: str
    description: str
    status: PlanStatus
    invite_code: str
    created_at: datetime
    members: list[MemberPublic] = []


class SessionOut(BaseModel):
    """Returned once on create/join. The frontend stores `member_token` in localStorage."""

    plan: PlanOut
    member: MemberPublic
    member_token: str


# ---------- private chat ----------
class ChatIn(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class MessageOut(ORM):
    id: str
    role: str
    content: str
    created_at: datetime


class ConstraintOut(ORM):
    """Only ever returned to the member who owns it."""

    id: str
    category: ConstraintCategory
    summary: str
    value: dict
    is_hard: bool


# ---------- proposals & votes ----------
class ProposalOut(ORM):
    id: str
    round: int
    title: str
    summary: str
    details: dict
    tradeoffs: list
    fit_score: int
    created_at: datetime


class VoteIn(BaseModel):
    score: int = Field(ge=1, le=3)
    comment: str = ""


class TallyOut(BaseModel):
    proposal_id: str
    total_score: int
    votes: int
