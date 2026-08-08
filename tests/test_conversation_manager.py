from app.services.agent.conversation import ConversationManager, MessageRole


def test_add_and_get_messages():
    manager = ConversationManager()

    manager.add_message(
        "conversation-1",
        MessageRole.USER,
        "Hello",
    )
    manager.add_message(
        "conversation-1",
        MessageRole.ASSISTANT,
        "Hi!",
    )

    assert manager.get_messages("conversation-1") == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]


def test_clear_messages():
    manager = ConversationManager()

    manager.add_message(
        "conversation-1",
        MessageRole.USER,
        "Hello",
    )
    manager.clear("conversation-1")

    assert manager.get_messages("conversation-1") == []


def test_get_messages_returns_copy():
    manager = ConversationManager()

    manager.add_message(
        "conversation-1",
        MessageRole.USER,
        "Hello",
    )

    messages = manager.get_messages("conversation-1")
    messages.clear()

    assert manager.get_messages("conversation-1") == [
        {"role": MessageRole.USER, "content": "Hello"},
    ]


def test_conversations_are_isolated():
    manager = ConversationManager()

    manager.add_message(
        "conversation-1",
        MessageRole.USER,
        "Hello from A",
    )
    manager.add_message(
        "conversation-2",
        MessageRole.USER,
        "Hello from B",
    )

    assert manager.get_messages("conversation-1") == [
        {"role": "user", "content": "Hello from A"},
    ]

    assert manager.get_messages("conversation-2") == [
        {"role": "user", "content": "Hello from B"},
    ]


def test_get_messages_for_unknown_conversation():
    manager = ConversationManager()

    assert manager.get_messages("unknown") == []


def test_clear_conversation():
    manager = ConversationManager()

    manager.add_message(
        "conversation-1",
        MessageRole.USER,
        "Hello",
    )

    manager.clear("conversation-1")

    assert manager.get_messages("conversation-1") == []
