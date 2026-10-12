"""A member's PRIVATE conversation with the interviewer agent."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents import interviewer
from app.auth import current_member, require_plan_member
from app.db import get_db
from app.models import Constraint, Member, Message
from app.schemas import ChatIn, ConstraintOut, MessageOut

router = APIRouter(tags=["chat"])


@router.get("/plans/{plan_id}/chat", response_model=list[MessageOut])
def get_my_chat(plan_id: str, member: Member = Depends(current_member), db: Session = Depends(get_db)):
    require_plan_member(plan_id, member)
    return db.scalars(select(Message).where(Message.member_id == member.id).order_by(Message.created_at)).all()


@router.get("/plans/{plan_id}/constraints", response_model=list[ConstraintOut])
def get_my_constraints(plan_id: str, member: Member = Depends(current_member), db: Session = Depends(get_db)):
    """Shows a member what the agent understood about THEM, so they can correct it."""
    require_plan_member(plan_id, member)
    return db.scalars(select(Constraint).where(Constraint.member_id == member.id)).all()


@router.post("/plans/{plan_id}/chat", response_model=MessageOut)
async def send_message(
    plan_id: str,
    body: ChatIn,
    member: Member = Depends(current_member),
    db: Session = Depends(get_db),
):
    """
    TODO (Week 2): implement.
      1. require_plan_member(...)
      2. Save the user's Message.
      3. Call `await interviewer.run_turn(db, member, body.content)`. It runs the tool
         loop, saves any Constraint rows, and returns the assistant's reply text.
      4. Save the assistant's Message and return it.
      5. If the agent called `finish_interview`, broadcast {"type": "interview_done", ...}.

    Stretch (Week 3): stream the reply token-by-token with StreamingResponse (SSE).
    """
    require_plan_member(plan_id, member)
    try:
        reply = await interviewer.run_turn(db, member, body.content)
    except NotImplementedError:
        raise HTTPException(501, "Interviewer agent not implemented yet (see BUILD_PLAN.md, Week 2)")
    return reply
