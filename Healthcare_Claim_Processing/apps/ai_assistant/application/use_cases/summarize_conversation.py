# ai_assistant/application/use_cases/summarize_conversation.py

from shared.application.result import Result

from ai_assistant.application.dto.ai_response_dto import AIResponseDTO

from ai_assistant.application.queries.get_conversation_history import (
    GetConversationHistoryQuery,
)

from ai_assistant.application.services.llm_service import (
    LLMService,
)

from ai_assistant.application.services.conversation_service import (
    ConversationService,
)


class SummarizeConversationUseCase:

    def __init__(
        self,
        llm_service: LLMService,
        conversation_service: ConversationService,
    ):
        self._llm_service = llm_service
        self._conversation_service = conversation_service

    async def execute(
        self,
        query: GetConversationHistoryQuery,
    ) -> Result[AIResponseDTO]:

        history = await self._conversation_service.get_history(
            query.conversation_id,
        )

        summary = await self._llm_service.summarize(history)

        return Result.success(summary)