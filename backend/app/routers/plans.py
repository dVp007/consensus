"""Plans and membership. These endpoints are implemented as a working reference
for the style used everywhere else; the TODO routers follow the same patterns."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import current_member, new_token, require_plan_member
from app.db import get_db
from app.models import Member, MemberRole, Plan, PlanStatus
from app.realtime import manager
from app.schemas import JoinPlan, MemberPublic, PlanCreate, PlanOut, SessionOut

router = APIRouter(tags=["plans"])


@router.post("/plans", response_model=SessionOut, status_code=201)
def create_plan(body: PlanCreate, db: Session = Depends(get_db)):
    raw, hashed = new_token()
    plan = Plan(title=body.title, description=body.description)
    organizer = Member(display_name=body.organizer_name, role=MemberRole.organizer, token_hash=hashed)
    plan.members.append(organizer)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return SessionOut(plan=PlanOut.model_validate(plan), member=MemberPublic.model_validate(organizer), member_token=raw)


@router.get("/invites/{invite_code}", response_model=PlanOut)
def preview_invite(invite_code: str, db: Session = Depends(get_db)):
    """Lets the join page show the plan title before someone enters their name."""
    plan = db.scalar(select(Plan).where(Plan.invite_code == invite_code))
    if plan is None:
        raise HTTPException(404, "Invite not found")
    return plan


@router.post("/invites/{invite_code}/join", response_model=SessionOut, status_code=201)
async def join_plan(invite_code: str, body: JoinPlan, db: Session = Depends(get_db)):
    plan = db.scalar(select(Plan).where(Plan.invite_code == invite_code))
    if plan is None:
        raise HTTPException(404, "Invite not found")
    if plan.status != PlanStatus.gathering:
        raise HTTPException(409, "This plan is no longer accepting new members")

    raw, hashed = new_token()
    member = Member(plan_id=plan.id, display_name=body.display_name, token_hash=hashed)
    db.add(member)
    db.commit()
    db.refresh(plan)

    member_out = MemberPublic.model_validate(member)
    await manager.broadcast(plan.id, {"type": "member_joined", "member": member_out.model_dump(mode="json")})
    return SessionOut(plan=PlanOut.model_validate(plan), member=member_out, member_token=raw)


@router.get("/plans/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: str, member: Member = Depends(current_member), db: Session = Depends(get_db)):
    require_plan_member(plan_id, member)
    return db.get(Plan, plan_id)


@router.get("/plans/{plan_id}/me", response_model=MemberPublic)
def get_me(plan_id: str, member: Member = Depends(current_member)):
    require_plan_member(plan_id, member)
    return member
