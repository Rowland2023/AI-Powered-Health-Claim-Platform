
from __future__ import annotations

from ai_assistant.application.services.conversation_service import (
    ConversationService,
)
from ai_assistant.application.services.llm_service import (
    LLMService,
)
from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)

from ai_assistant.application.use_cases.execute_ai_request import (
    ExecuteAIRequestUseCase,
)
from ai_assistant.application.use_cases.execute_tool_call import (
    ExecuteToolCallUseCase,
)
from ai_assistant.application.use_cases.explain_tool import (
    ExplainToolUseCase,
)
from ai_assistant.application.use_cases.list_tools import (
    ListToolsUseCase,
)
from ai_assistant.application.use_cases.summarize_conversation import (
    SummarizeConversationUseCase,
)
from ai_assistant.application.use_cases.get_conversation_history import (
    GetConversationHistoryUseCase,
)

from ai_assistant.presentation.http.controllers.ai_assistant import (
    AIController,
)

from ai_assistant.presentation.http.presenters.ai_response_presenter import (
    AIResponsePresenter,
)
from ai_assistant.presentation.http.presenters.conversation_presenter import (
    ConversationPresenter,
)
from ai_assistant.presentation.http.presenters.tool_presenter import (
    ToolPresenter,
)


def create_ai_dependencies(
    *,
    llm_service: LLMService,
    tool_execution_service: ToolExecutionService,
    conversation_service: ConversationService,
    conversation_history_use_case: GetConversationHistoryUseCase,
) -> dict:
    """
    Composition root for the AI Assistant bounded context.

    Infrastructure dependencies are supplied by the application
    bootstrap.

    This function wires:

        Application Services
                ↓
           Use Cases
                ↓
            Presenters
                ↓
           Controller
    """

    # =========================================================
    # USE CASES
    # =========================================================

    execute_ai_request = ExecuteAIRequestUseCase(
        llm_service=llm_service,
        tool_execution_service=tool_execution_service,
        conversation_service=conversation_service,
    )

    execute_tool_call = ExecuteToolCallUseCase(
        tool_execution_service=tool_execution_service,
    )

    list_tools = ListToolsUseCase(
        tool_execution_service=tool_execution_service,
    )

    explain_tool = ExplainToolUseCase(
        tool_execution_service=tool_execution_service,
    )

    summarize_conversation = SummarizeConversationUseCase(
        llm_service=llm_service,
        conversation_service=conversation_service,
    )

    # =========================================================
    # PRESENTERS
    # =========================================================

    ai_response_presenter = AIResponsePresenter()

    conversation_presenter = ConversationPresenter()

    tool_presenter = ToolPresenter()

    # =========================================================
    # CONTROLLER
    # =========================================================

    ai_controller = AIController(
        execute_ai_request=execute_ai_request,
        execute_tool_call=execute_tool_call,
        list_tools=list_tools,
        explain_tool=explain_tool,
        summarize_conversation=summarize_conversation,
        conversation_history=conversation_history_use_case,
        ai_response_presenter=ai_response_presenter,
        conversation_presenter=conversation_presenter,
        tool_presenter=tool_presenter,
    )

    # =========================================================
    # DEPENDENCY CONTAINER
    # =========================================================

    return {
        "execute_ai_request": execute_ai_request,
        "execute_tool_call": execute_tool_call,
        "list_tools": list_tools,
        "explain_tool": explain_tool,
        "summarize_conversation": summarize_conversation,
        "conversation_history": conversation_history_use_case,

        "ai_response_presenter": ai_response_presenter,
        "conversation_presenter": conversation_presenter,
        "tool_presenter": tool_presenter,

        "ai_controller": ai_controller,
    }
