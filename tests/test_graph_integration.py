import pytest
from app.agent.graph import run_agent
from app.agent.llm import LLMClient
from app.agent.state import AgentState


@pytest.mark.integration
def test_run_agent_end_to_end_with_real_openai(require_openai_key):
    llm = LLMClient()
    state: AgentState = {
        "user_input": "Say hello in five words or fewer.",
        "prompt_version": "v1",
    }

    result = run_agent(state, llm)

    assert "final_answer" in result
    assert isinstance(result["final_answer"], str)
    assert len(result["final_answer"]) > 0