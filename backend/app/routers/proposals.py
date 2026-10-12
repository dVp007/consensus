"""Planner agent run, proposals, and voting."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import current_member, require_organizer, require_plan_member
from app.db import get_db
from app.models import Member, Proposal
from app.schemas import ProposalOut, TallyOut, VoteIn

router = APIRouter(tags=["proposals"])


@router.post("/plans/{plan_id}/propose", status_code=202)
async def start_planning(
    plan_id: str,
    background: BackgroundTasks,
    member: Member = Depends(current_member),
    db: Session = Depends(get_db),
):
    """
    TODO (Week 3): implement.
      1. require_organizer(...). Optionally require that most members have interview_done.
      2. Set plan.status = proposing, broadcast status_changed.
      3. background.add_task(planner.run_planner, plan_id)  -- agent runs outside the request.
         run_planner should open its OWN db session (SessionLocal()), not reuse this one.
      4. Return {"status": "started"} right away. Progress arrives over the WebSocket.

    Stretch: replace BackgroundTasks with a real job queue (arq / Celery + Redis).
    """
    require_organizer(plan_id, member)
    raise HTTPException(501, "Planner not implemented yet (see BUILD_PLAN.md, Week 3)")


@router.get("/plans/{plan_id}/proposals", response_model=list[ProposalOut])
def list_proposals(plan_id: str, member: Member = Depends(current_member), db: Session = Depends(get_db)):
    require_plan_member(plan_id, member)
    return db.scalars(
        select(Proposal).where(Proposal.plan_id == plan_id).order_by(Proposal.round.desc(), Proposal.fit_score.desc())
    ).all()


@router.put("/proposals/{proposal_id}/vote", status_code=204)
async def vote(
    proposal_id: str,
    body: VoteIn,
    member: Member = Depends(current_member),
    db: Session = Depends(get_db),
):
    """
    TODO (Week 4): implement.
      1. Load the proposal, require_plan_member(proposal.plan_id, member).
      2. Upsert the Vote (one per member per proposal, see UniqueConstraint).
      3. Broadcast {"type": "vote_cast", "proposal_id": ...} (not who voted what!).
      4. If every member has voted on every proposal, set plan.status = decided.
    """
    raise HTTPException(501, "Voting not implemented yet (see BUILD_PLAN.md, Week 4)")


@router.get("/plans/{plan_id}/tally", response_model=list[TallyOut])
def tally(plan_id: str, member: Member = Depends(current_member), db: Session = Depends(get_db)):
    """TODO (Week 4): sum Vote.score per proposal with a GROUP BY query."""
    require_plan_member(plan_id, member)
    raise HTTPException(501, "Tally not implemented yet (see BUILD_PLAN.md, Week 4)")
