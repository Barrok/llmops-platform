from app.services.agent.conversation import ConversationManager, MessageRole
from app.services.agent.prompts import PromptManager
from app.services.llm.base import LLMClient


class AgentService:
    """Core agent orchestration service."""

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_manager: PromptManager,
        conversation_manager: ConversationManager,
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.conversation_manager = conversation_manager

    def chat(self, conversation_id: str, message: str) -> str:
        if not self.conversation_manager.get_messages(conversation_id):
            self.conversation_manager.add_message(
                conversation_id,
                MessageRole.SYSTEM,
                self.prompt_manager.get_system_prompt(),
            )

        self.conversation_manager.add_message(
            conversation_id,
            MessageRole.USER,
            message,
        )

        response = self.llm_client.generate(
            self.conversation_manager.get_messages(conversation_id)
        )

        self.conversation_manager.add_message(
            conversation_id,
            MessageRole.ASSISTANT,
            response,
        )

        return response
