"""Interviewer agent: one private conversation per member.

Implement `run_turn` (Week 2). Suggested shape of the agent loop:

    messages = [system prompt] + this member's previous Messages + the new user message
    for step in range(settings.agent_max_steps):          # guardrail: never loop forever
        msg = await llm.complete(messages, tools=INTERVIEWER_TOOLS)
        if not msg.tool_calls:
            return msg.content                             # model replied with text: done
        messages.append(msg)                               # keep the assistant's tool request
        for call in msg.tool_calls:
            result = execute_tool(db, member, call.function.name, call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return "fallback text"                                 # hit the step limit

Things that will bite you (and are great to mention in interviews):
  * `call.function.arguments` is a JSON STRING and may be invalid. Catch json errors and
    return an error string to the model as the tool result so it can retry.
  * Validate `category` against ConstraintCategory before saving.
  * Some models (especially free ones) handle tools poorly. Test a few on OpenRouter.
"""

from sqlalchemy.orm import Session

from app.agents import llm  # noqa: F401
from app.agents.prompts import INTERVIEWER_SYSTEM  # noqa: F401
from app.agents.tools import INTERVIEWER_TOOLS  # noqa: F401
from app.config import get_settings
from app.models import Member

settings = get_settings()


def execute_tool(db: Session, member: Member, name: str, raw_arguments: str) -> str:
    """Run one tool call and return a short string result for the model.

    TODO (Week 2):
      * "save_constraint": json.loads the arguments, create a Constraint row, return "saved".
      * "finish_interview": set member.interview_done = True, return "done".
      * unknown name: return an error string (don't raise; let the model recover).
    """
    raise NotImplementedError


async def run_turn(db: Session, member: Member, user_text: str):
    """Process one user message and return the saved assistant Message. See module docstring."""
    raise NotImplementedError
