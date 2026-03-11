from typing import Literal, cast

from app.agent.state import AgentState
from app.agent.prompts import get_prompt
from app.agent.tools import weather_tool
from app.agent.llm import LLMClient


def route_intent(state: AgentState) -> str:
    if state.get("intent") == "search_docs":
        return "tool_node"
    return "answer_node"


def classify_node(state: AgentState, llm: LLMClient) -> AgentState:
    prompt = get_prompt(state["prompt_version"])
    intent = llm.classify_intent(prompt["system"], state["user_input"])
    classified_intent = cast(Literal["search_docs", "smalltalk", "unknown"], intent if intent in {"search_docs", "smalltalk"} else "unknown")
    return {
        **state,
        "intent": classified_intent,
        "trace": [*(state.get("trace", [])), "classify_node"],
    }


def tool_node(state: AgentState) -> AgentState:
    result = weather_tool(state["user_input"])
    return {
        **state,
        "tool_result": result,
        "trace": [*(state.get("trace", [])), "tool_node"],
    }


def answer_node(state: AgentState, llm: LLMClient) -> AgentState:
    prompt = get_prompt(state["prompt_version"])
    final_answer = llm.answer(
        prompt["system"],
        state["user_input"],
        state.get("tool_result"),
    )
    return {
        **state,
        "final_answer": final_answer,
        "trace": [*(state.get("trace", [])), "answer_node"],
    }


def run_agent(state: AgentState, llm: LLMClient) -> AgentState:
    state = classify_node(state, llm)
    next_node = route_intent(state)
    if next_node == "tool_node":
        state = tool_node(state)
    state = answer_node(state, llm)
    return state