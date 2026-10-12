"""Tests for services/scoring.py. They're marked xfail until you implement it;
delete the marker once your implementation passes."""

import pytest

from app.services.scoring import MemberConstraint, score_proposal

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Week 3: implement score_proposal")


def test_everyone_within_budget_scores_high():
    constraints = {
        "P1": [MemberConstraint("budget", {"max_usd": 400}, True)],
        "P2": [MemberConstraint("budget", {"max_usd": 300}, True)],
    }
    assert score_proposal({"cost_per_person_usd": 250}, constraints) >= 80


def test_breaking_a_hard_budget_scores_low():
    constraints = {
        "P1": [MemberConstraint("budget", {"max_usd": 400}, True)],
        "P2": [MemberConstraint("budget", {"max_usd": 150}, True)],
    }
    assert score_proposal({"cost_per_person_usd": 250}, constraints) < 50
