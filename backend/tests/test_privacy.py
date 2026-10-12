import pytest

from app.agents.privacy import find_leaks

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Week 4: implement find_leaks")


def test_flags_member_name():
    assert find_leaks("Ben can only spend $150", ["Asha", "Ben"])


def test_anonymous_text_is_safe():
    assert find_leaks("One person has a tighter budget, so option B is cheaper.", ["Asha", "Ben"]) == []


def test_short_names_need_word_boundaries():
    # "Al" must not match inside "totally"
    assert find_leaks("This is totally affordable.", ["Al"]) == []
