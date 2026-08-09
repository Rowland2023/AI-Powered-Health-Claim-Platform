
from __future__ import annotations

from uuid import UUID

from ai_assistant.application.commands.execute_prompt import (
    ExecutePromptCommand,
)
from ai_assistant.application.commands.execute_tool import (
    ExecuteToolCommand,
)

from ai_assistant.application.queries.get_tool_definition import (
    GetToolDefinitionQuery,
)
from ai_assistant.application.queries.list_available_tools import (
    ListAvailableToolsQuery,
)
from ai_assistant.application.queries.get_conversation_history import (
    GetConversationHistoryQuery,
)
from ai_assistant.application.queries.summarize_conversation import (
    SummarizeConversationQuery,
)

from ai_assistant.application.use_cases.execute_ai_request import (
    ExecuteAIRequestUseCase,
)
from ai_assistant.application.use_cases.execute_tool_call import (
    ExecuteToolCallUseCase,
)
from ai_assistant.application.use_cases.list_tools import (
    ListToolsUseCase,
)
from ai_assistant.application.use_cases.explain_tool import (
    ExplainToolUseCase,
)
from ai_assistant.application.use_cases.summarize_conversation import (
    SummarizeConversationUseCase,
)
from ai_assistant.application.use_cases.get_conversation_history import (
    GetConversationHistoryUseCase,
)

from ...presenters.ai_response_presenter import (
    AIResponsePresenter,
)
from ...presenters.conversation_presenter import (
    ConversationPresenter,
)
from ...presenters.tool_presenter import (
    ToolPresenter,
)

from ...serializers.ai_request_serializer import (
    AIRequestSerializer,
)
from ...serializers.tool_call_serializer import (
    ToolCallSerializer,
)


class AIController:
    """
    HTTP controller for the AI Assistant bounded context.

    Responsibilities:

        HTTP serializer
            ↓
        Application command/query
            ↓
        Use case
            ↓
        Presenter
            ↓
        HTTP response data

    The controller does not contain business logic.
    """

    def __init__(
        self,
        execute_ai_request: ExecuteAIRequestUseCase,
        execute_tool_call: ExecuteToolCallUseCase,
        list_tools: ListToolsUseCase,
        explain_tool: ExplainToolUseCase,
        summarize_conversation: SummarizeConversationUseCase,
        conversation_history: GetConversationHistoryUseCase,
        ai_response_presenter: AIResponsePresenter,
        conversation_presenter: ConversationPresenter,
        tool_presenter: ToolPresenter,
    ) -> None:

        self._execute_ai_request = execute_ai_request
        self._execute_tool_call = execute_tool_call
        self._list_tools = list_tools
        self._explain_tool = explain_tool
        self._summarize_conversation = summarize_conversation
        self._conversation_history = conversation_history

        self._ai_response_presenter = (
            ai_response_presenter
        )

        self._conversation_presenter = (
            conversation_presenter
        )

        self._tool_presenter = (
            tool_presenter
        )

    # =========================================================
    # CHAT
    # =========================================================

    async def chat(
        self,
        serializer: AIRequestSerializer,
        user_id: UUID,
    ):

        command = ExecutePromptCommand(
            prompt=serializer.prompt,
            user_id=user_id,
            conversation_id=serializer.conversation_id,
            temperature=serializer.temperature,
            max_tokens=serializer.max_tokens,
        )

        result = await self._execute_ai_request.execute(
            command
        )

        return self._ai_response_presenter.present(
            result
        )

    # =========================================================
    # EXECUTE TOOL
    # =========================================================

    async def execute_tool(
        self,
        serializer: ToolCallSerializer,
    ):

        command = ExecuteToolCommand(
            tool_name=serializer.tool_name,
            arguments=serializer.arguments,
        )

        result = await self._execute_tool_call.execute(
            command
        )

        return self._ai_response_presenter.present(
            result
        )

    # =========================================================
    # LIST TOOLS
    # =========================================================

    async def list_tools(self):

        query = ListAvailableToolsQuery()

        result = await self._list_tools.execute(
            query
        )

        return self._tool_presenter.present(
            result
        )

    # =========================================================
    # EXPLAIN TOOL
    # =========================================================

    async def explain_tool(
        self,
        tool_name: str,
    ):

        query = GetToolDefinitionQuery(
            tool_name=tool_name,
        )

        result = await self._explain_tool.execute(
            query
        )

        return self._tool_presenter.present(
            result
        )

    # =========================================================
    # CONVERSATION HISTORY
    # =========================================================

    async def history(
        self,
        conversation_id: UUID,
    ):

        query = GetConversationHistoryQuery(
            conversation_id=conversation_id,
        )

        result = await self._conversation_history.execute(
            query
        )

        return self._conversation_presenter.present(
            result
        )

    # =========================================================
    # SUMMARIZE CONVERSATION
    # =========================================================

    async def summarize(
        self,
        conversation_id: UUID,
    ):

        query = SummarizeConversationQuery(
            conversation_id=conversation_id,
        )

        result = await self._summarize_conversation.execute(
            query
        )

        return self._conversation_presenter.present(
            result
        )
