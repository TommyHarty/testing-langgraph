import pytest
from app.agent.prompts import get_prompt


@pytest.mark.parametrize(
    ("version", "expected_fragment"),
    [
        ("v1", "Use tools only when needed"),
        ("v2", "Prefer tools for factual lookups"),
    ],
)
def test_get_prompt_returns_expected_prompt(version, expected_fragment):
    prompt = get_prompt(version)
    assert expected_fragment in prompt["system"]


def test_get_prompt_raises_for_unknown_version():
    with pytest.raises(ValueError, match="Unknown prompt version"):
        get_prompt("v999")