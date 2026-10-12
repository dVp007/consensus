"""Planner agent: reads every member's constraints and proposes options for the group.

Implement `run_planner` (Week 3). Suggested pipeline:

  1. Load all members + constraints for the plan.
  2. ANONYMIZE: label members P1..Pn (shuffle the order!) and drop names entirely.
     Build a compact text/JSON block of constraints per label.
  3. Call llm.complete with PLANNER_SYSTEM and ask for JSON
     (try response_format={"type": "json_object"} if your model supports it).
  4. Parse + validate with a Pydantic model. If invalid, retry once with the error message.
  5. For each option: fit_score = scoring.score_proposal(...)  (deterministic Python, not LLM)
  6. privacy.check(...) every title/summary/tradeoff. If it leaks, regenerate or redact.
  7. Save Proposal rows, set plan.status = voting, broadcast status_changed.

Broadcast {"type": "agent_step", "step": "..."} between stages so the UI shows live progress.
On any exception: set status back to gathering and broadcast {"type": "planner_failed"}.
"""

from app.agents import llm  # noqa: F401
from app.agents.prompts import PLANNER_SYSTEM  # noqa: F401


async def run_planner(plan_id: str) -> None:
    """Runs in the background. Open your own session: `with SessionLocal() as db:`."""
    raise NotImplementedError
