from app.models.chunk import DocumentChunk
from app.services.agent.conversation import ConversationManager, MessageRole
from app.services.agent.prompts import PromptManager
from app.services.llm.base import LLMClient
from app.services.rag.context import ContextBuilder
from app.services.retrieval.service import RetrievalService


class AgentService:
    """Core agent orchestration service."""

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_manager: PromptManager,
        conversation_manager: ConversationManager,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.conversation_manager = conversation_manager
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder

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

        chunks = self.retrieval_service.retrieve(
            query=message,
            limit=5,
        )

        context = self.context_builder.build(chunks)

        if context:
            prompt = f"Context:\n{context}\n\nQuestion:\n{message}"
        else:
            prompt = message

        messages = self.conversation_manager.get_messages(conversation_id)

        messages[-1] = {
            "role": MessageRole.USER.value,
            "content": prompt,
        }

        response = self.llm_client.generate(messages)

        self.conversation_manager.add_message(
            conversation_id,
            MessageRole.ASSISTANT,
            response,
        )

        return response

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
    ) -> list[DocumentChunk]:
        return self.retrieval_service.retrieve(
            query=query,
            limit=limit,
        )
