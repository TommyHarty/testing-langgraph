from app.agent.graph import run_agent
from app.agent.llm import LLMClient


class VersionSensitiveFakeLLM(LLMClient):
    def __init__(self) -> None:
        pass  # skip OpenAI client initialisation

    def classify_intent(self, system_prompt: str, user_input: str) -> str:
        if "Prefer tools for factual lookups" in system_prompt:
            return "search_docs"
        return "smalltalk"

    def answer(self, system_prompt: str, user_input: str, tool_result: str | None = None) -> str:
        return "ok"


def test_v1_does_not_prefer_tool():
    llm = VersionSensitiveFakeLLM()
    result = run_agent(
        {"user_input": "What's the weather in London?", "prompt_version": "v1"},
        llm,
    )
    assert result.get("intent") == "smalltalk"
    assert result.get("trace") == ["classify_node", "answer_node"]


def test_v2_prefers_tool():
    llm = VersionSensitiveFakeLLM()
    result = run_agent(
        {"user_input": "What's the weather in London?", "prompt_version": "v2"},
        llm,
    )
    assert result.get("intent") == "search_docs"
    assert result.get("trace") == ["classify_node", "tool_node", "answer_node"]