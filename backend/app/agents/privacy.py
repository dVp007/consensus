"""Privacy guard: make sure planner output never exposes who said what.

This is the feature that makes Consensus different from a normal chatbot. Build it in
two layers (Week 4):

  1. Deterministic check (start here): fail if any member's display_name appears in the
     text, or if a constraint's exact summary string is copied verbatim next to a name.
  2. LLM judge (stretch): ask a second model call "Could a group member infer which
     specific person holds any of these constraints? Answer JSON {leak: bool, reason}".

Write tests for it in tests/test_privacy.py. Leaks are the bug you most want to catch.
"""


def find_leaks(text: str, member_names: list[str]) -> list[str]:
    """Return a list of human-readable problems found in `text` (empty list = safe).

    TODO (Week 4): case-insensitive name matching, watch out for short names like "Al"
    matching inside other words (use word boundaries: re.search(rf"\\b{re.escape(n)}\\b", ...)).
    """
    raise NotImplementedError
