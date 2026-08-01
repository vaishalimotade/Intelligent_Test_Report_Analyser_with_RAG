import os

import pytest

from backend.app.services.llm import LLMService, build_prompt


class DummyResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return type("Response", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": '{"summary": "ok"}'} )()})()]})()


def test_build_prompt_uses_default_template():
    prompt = build_prompt("failed tests")
    assert "QA analyst" in prompt
    assert "failed tests" in prompt


def test_generate_text_uses_openai_compatible_client(monkeypatch):
    dummy = DummyResponses()

    class DummyClient:
        def __init__(self, *args, **kwargs):
            self.chat = type("Chat", (), {"completions": dummy})()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("backend.app.services.llm.OpenAI", DummyClient)

    service = LLMService()
    result = service.generate_text("Analyze this report", system_prompt="You are a QA assistant")

    assert result == {"summary": "ok"}
    assert dummy.calls[0]["messages"][0]["content"] == "You are a QA assistant"
