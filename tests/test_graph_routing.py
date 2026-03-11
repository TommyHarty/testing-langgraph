from typing import cast

from app.agent.graph import route_intent, run_agent
from app.agent.llm import LLMClient
from app.agent.state import AgentState


class FakeLLM(LLMClient):
    def __init__(self) -> None:
        pass  # skip OpenAI client initialisation

    def classify_intent(self, system_prompt: str, user_input: str) -> str:
        if "weather" in user_input.lower():
            return "search_docs"
        return "smalltalk"

    def answer(self, system_prompt: str, user_input: str, tool_result: str | None = None) -> str:
        if tool_result:
            return f"Used tool: {tool_result}"
        return "No tool needed"


def test_route_intent_to_tool_node():
    state = cast(AgentState, {"intent": "search_docs"})
    assert route_intent(state) == "tool_node"


def test_route_intent_to_answer_node():
    state = cast(AgentState, {"intent": "smalltalk"})
    assert route_intent(state) == "answer_node"


def test_run_agent_uses_tool_when_classified_for_tool():
    llm = FakeLLM()
    state: AgentState = {
        "user_input": "What is the weather in London?",
        "prompt_version": "v1",
    }

    result = run_agent(state, llm)

    assert result.get("intent") == "search_docs"
    assert "tool_result" in result
    assert result.get("trace") == ["classify_node", "tool_node", "answer_node"]
    assert "Used tool:" in result.get("final_answer", "")


def test_run_agent_skips_tool_for_smalltalk():
    llm = FakeLLM()
    state: AgentState = {
        "user_input": "hello mate",
        "prompt_version": "v1",
    }

    result = run_agent(state, llm)

    assert result.get("intent") == "smalltalk"
    assert "tool_result" not in result
    assert result.get("trace") == ["classify_node", "answer_node"]
    assert result.get("final_answer") == "No tool needed"