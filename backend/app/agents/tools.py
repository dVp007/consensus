"""Tool (function) schemas the interviewer agent can call, in OpenAI tool format.

The model decides WHEN to call them; your code decides WHAT they do. That split is the
heart of an agent, so the execution side lives in interviewer.py for you to write.
"""

from app.models import ConstraintCategory

SAVE_CONSTRAINT = {
    "type": "function",
    "function": {
        "name": "save_constraint",
        "description": "Record one concrete preference or limit the user just shared.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": [c.value for c in ConstraintCategory]},
                "summary": {"type": "string", "description": "Short, neutral, e.g. 'Max $400 total'"},
                "value": {
                    "type": "object",
                    "description": "Machine-readable form, e.g. {\"max_usd\": 400} or "
                    "{\"available\": [\"2026-11-06\", \"2026-11-08\"]}",
                },
                "is_hard": {"type": "boolean", "description": "True only if non-negotiable"},
            },
            "required": ["category", "summary", "is_hard"],
        },
    },
}

FINISH_INTERVIEW = {
    "type": "function",
    "function": {
        "name": "finish_interview",
        "description": "Call once you have enough information from this person.",
        "parameters": {"type": "object", "properties": {}},
    },
}

INTERVIEWER_TOOLS = [SAVE_CONSTRAINT, FINISH_INTERVIEW]

# TODO (Week 6, stretch): planner tools, e.g. `search_places` (Google Places / Foursquare),
# `get_weather`, or `estimate_travel_cost`, so proposals use real data instead of guesses.
