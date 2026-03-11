PROMPTS = {
    "v1": {
        "system": "You are a concise assistant. Use tools only when needed."
    },
    "v2": {
        "system": "You are a precise assistant. Prefer tools for factual lookups."
    },
}


def get_prompt(version: str) -> dict:
    if version not in PROMPTS:
        raise ValueError(f"Unknown prompt version: {version}")
    return PROMPTS[version]
