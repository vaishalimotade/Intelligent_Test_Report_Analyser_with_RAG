import json
import os
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None


DEFAULT_SYSTEM_PROMPT = "You are a QA analyst helping summarize CI/CD test results."
DEFAULT_USER_PROMPT_TEMPLATE = """
You are a QA analyst.
Analyze the following test report context and provide a concise summary with actionable insights.

Context:
{context}
"""


def build_prompt(context: str, system_prompt: Optional[str] = None, user_template: Optional[str] = None) -> str:
    if not context or not context.strip():
        raise ValueError("context must not be empty")

    prompt_template = user_template or DEFAULT_USER_PROMPT_TEMPLATE
    system = system_prompt or DEFAULT_SYSTEM_PROMPT
    return prompt_template.format(context=context, system_prompt=system)


class LLMService:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        self.model = model or os.getenv("MODEL_NAME") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = None
        if OpenAI is not None and self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_text(self, context: str, system_prompt: Optional[str] = None, user_template: Optional[str] = None) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("LLM client is not configured. Set OPENAI_API_KEY and optionally LLM_BASE_URL.")

        prompt = build_prompt(context, system_prompt=system_prompt, user_template=user_template)
        messages = [
            {"role": "system", "content": system_prompt or DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        content = getattr(response.choices[0].message, "content", None) or "{}"
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return parsed
            return {"summary": parsed}
        except json.JSONDecodeError:
            return {"summary": content}
