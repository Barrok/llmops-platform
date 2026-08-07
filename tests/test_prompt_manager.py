from app.services.agent.prompts import PromptManager


def test_default_system_prompt():
    manager = PromptManager()

    prompt = manager.get_system_prompt()

    assert "helpful AI assistant" in prompt
    assert len(prompt) > 0
