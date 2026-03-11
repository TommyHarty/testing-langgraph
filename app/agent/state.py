from typing import TypedDict, Literal


class AgentState(TypedDict, total=False):
    user_input: str
    prompt_version: str
    intent: Literal["search_docs", "smalltalk", "unknown"]
    tool_result: str
    final_answer: str
    trace: list[str]