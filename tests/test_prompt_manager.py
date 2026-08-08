from app.services.agent.prompts import PromptManager


def test_build_messages():
    manager = PromptManager()

    messages = manager.build_messages("Explain Kubernetes")

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == manager.get_system_prompt()
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Explain Kubernetes"


def test_custom_system_prompt():
    manager = PromptManager(system_prompt="You are a DevOps expert.")

    assert manager.get_system_prompt() == "You are a DevOps expert."


def test_custom_system_prompt_is_used_in_messages():
    manager = PromptManager(system_prompt="You are a DevOps expert.")

    messages = manager.build_messages("Explain Kubernetes")

    assert messages[0] == {
        "role": "system",
        "content": "You are a DevOps expert.",
    }
