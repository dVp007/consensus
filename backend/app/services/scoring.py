"""Deterministic fit scoring. Don't let the LLM grade its own proposals: compute it.

Week 3 task. Start simple and make it smarter later:

  * For each member, check each HARD constraint against the proposal details.
    A violated hard constraint for anyone should drag the score down a lot.
  * Soft constraints add smaller bonuses/penalties.
  * Return 0-100.

Start with just `budget` (compare details["cost_per_person_usd"] to value["max_usd"]),
since it's numeric and easy to test. Add dates next (set intersection).
"""

from dataclasses import dataclass


@dataclass
class MemberConstraint:
    category: str
    value: dict
    is_hard: bool


def score_proposal(details: dict, constraints_by_member: dict[str, list[MemberConstraint]]) -> int:
    """TODO (Week 3). Pure function: no DB, no LLM. Easy to unit test."""
    raise NotImplementedError
