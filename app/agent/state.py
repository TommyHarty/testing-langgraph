from typing import TypedDict, Literal


class BaseAgentState(TypedDict):
    user_input: str
    prompt_version: str


class AgentState(BaseAgentState, total=False):
    intent: Literal["search_docs", "smalltalk", "unknown"]
    tool_result: str
    final_answer: str
    trace: list[str]