from types import SimpleNamespace
from app.agent.llm import LLMClient


def test_answer_sends_expected_payload(monkeypatch):
    captured = {}

    class FakeResponsesAPI:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="Final answer")

    class FakeOpenAIClient:
        def __init__(self):
            self.responses = FakeResponsesAPI()

    monkeypatch.setattr("app.agent.llm.OpenAI", lambda: FakeOpenAIClient())

    llm = LLMClient()
    result = llm.answer(
        "system-v2",
        "What is the weather?",
        "Weather for London: 12C and cloudy"
    )

    assert result == "Final answer"
    assert captured["model"] == "gpt-5-mini"
    assert captured["input"][0]["content"] == "system-v2"
    assert "Tool result: Weather for London: 12C and cloudy" in captured["input"][1]["content"]