from types import SimpleNamespace
from app.agent.llm import LLMClient


class FakeResponsesAPI:
    def create(self, **kwargs):
        return SimpleNamespace(output_text="smalltalk")


class FakeOpenAIClient:
    def __init__(self):
        self.responses = FakeResponsesAPI()


def test_classify_intent_monkeypatched(monkeypatch):
    monkeypatch.setattr("app.agent.llm.OpenAI", lambda: FakeOpenAIClient())

    llm = LLMClient()
    result = llm.classify_intent(
        "You are a concise assistant.",
        "hello there"
    )

    assert result == "smalltalk"