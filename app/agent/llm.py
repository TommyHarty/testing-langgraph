from openai import OpenAI


class LLMClient:
    def __init__(self) -> None:
        self.client = OpenAI()

    def classify_intent(self, system_prompt: str, user_input: str) -> str:
        response = self.client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classify intent: {user_input}"},
            ],
        )
        return response.output_text.strip()

    def answer(self, system_prompt: str, user_input: str, tool_result: str | None = None) -> str:
        extra = f"\nTool result: {tool_result}" if tool_result else ""
        response = self.client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {user_input}{extra}"},
            ],
        )
        return response.output_text.strip()