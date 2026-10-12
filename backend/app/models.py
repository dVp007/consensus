"""Database schema.

Privacy model (the core idea of Consensus):
  * Messages and Constraints belong to ONE member and are never returned to other members.
  * Only the planner agent sees everyone's constraints, and its output passes through a
    privacy check before anyone sees it.
"""

import enum
import secrets
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _invite_code() -> str:
    return secrets.token_urlsafe(6)


class PlanStatus(str, enum.Enum):
    gathering = "gathering"    # members chatting with the agent privately
    proposing = "proposing"    # planner agent is generating options
    voting = "voting"          # group votes on proposals
    decided = "decided"


class MemberRole(str, enum.Enum):
    organizer = "organizer"
    member = "member"


class ConstraintCategory(str, enum.Enum):
    budget = "budget"
    dates = "dates"
    location = "location"
    food = "food"
    accessibility = "accessibility"
    activity = "activity"
    dealbreaker = "dealbreaker"
    other = "other"


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus), default=PlanStatus.gathering)
    invite_code: Mapped[str] = mapped_column(String(32), unique=True, default=_invite_code)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    members: Mapped[list["Member"]] = relationship(back_populates="plan", cascade="all, delete-orphan")
    proposals: Mapped[list["Proposal"]] = relationship(back_populates="plan", cascade="all, delete-orphan")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"), index=True)
    display_name: Mapped[str] = mapped_column(String(80))
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole), default=MemberRole.member)
    # Lightweight auth: a random secret given to the browser once, stored hashed.
    # TODO (stretch): replace with real accounts (OAuth / magic link).
    token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    interview_done: Mapped[bool] = mapped_column(Boolean, default=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    plan: Mapped[Plan] = relationship(back_populates="members")
    messages: Mapped[list["Message"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    constraints: Mapped[list["Constraint"]] = relationship(back_populates="member", cascade="all, delete-orphan")


class Message(Base):
    """One turn in a member's PRIVATE chat with the interviewer agent."""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(16))  # "user" | "assistant"
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    member: Mapped[Member] = relationship(back_populates="messages")


class Constraint(Base):
    """A structured preference the interviewer agent extracted via a tool call."""

    __tablename__ = "constraints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    category: Mapped[ConstraintCategory] = mapped_column(Enum(ConstraintCategory))
    summary: Mapped[str] = mapped_column(String(300))  # e.g. "Max $400 total"
    value: Mapped[dict] = mapped_column(JSON, default=dict)  # e.g. {"max_usd": 400}
    is_hard: Mapped[bool] = mapped_column(Boolean, default=False)  # dealbreaker vs. preference
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    member: Mapped[Member] = relationship(back_populates="constraints")


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"), index=True)
    round: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSON, default=dict)     # cost, dates, itinerary...
    tradeoffs: Mapped[list] = mapped_column(JSON, default=list)   # anonymized, e.g. "2 people stretch budget"
    fit_score: Mapped[int] = mapped_column(Integer, default=0)    # 0-100 from services/scoring.py
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    plan: Mapped[Plan] = relationship(back_populates="proposals")
    votes: Mapped[list["Vote"]] = relationship(back_populates="proposal", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("proposal_id", "member_id", name="one_vote_per_member"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    proposal_id: Mapped[str] = mapped_column(ForeignKey("proposals.id", ondelete="CASCADE"), index=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    score: Mapped[int] = mapped_column(Integer)  # 1 = no, 2 = ok, 3 = love it
    comment: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    proposal: Mapped[Proposal] = relationship(back_populates="votes")
