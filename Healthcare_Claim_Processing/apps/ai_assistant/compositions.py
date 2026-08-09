
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

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

from ai_assistant.domain.tool_registry import ToolRegistry

from ai_assistant.infrastructure.llm.openai_client import (
    OpenAIClient,
)

from ai_assistant.infrastructure.persistence.repositories.postgres_conversation_repository import (
    PostgresConversationRepository,
)

from ai_assistant.infrastructure.services.postgres_conversation_service import (
    PostgresConversationService,
)

from ai_assistant.presentation.http.controllers.ai_assistant_controller import (
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

from ai_assistant.tools.patient.register_patient_tool import (
    RegisterPatientTool,
)
from ai_assistant.tools.patient.find_patient_tool import (
    FindPatientTool,
)


def create_ai_assistant_dependencies(
    *,
    session: AsyncSession,
    openai_api_key: str,
    register_patient_use_case,
    find_patient_use_case,
) -> dict:
    """
    Composition root for the AI Assistant bounded context.

    This function wires infrastructure implementations into
    application ports and application use cases.

    Nothing in the domain layer is instantiated here directly.

    Dependency direction:

        Infrastructure
             ↓
        Application
             ↓
        Presentation

    The composition root is the place where those dependencies
    are connected.
    """

    # =========================================================
    # INFRASTRUCTURE
    # =========================================================

    conversation_repository = (
        PostgresConversationRepository(
            session=session,
        )
    )

    conversation_service: ConversationService = (
        PostgresConversationService(
            repository=conversation_repository,
        )
    )

    llm_service: LLMService = OpenAIClient(
        api_key=openai_api_key,
    )

    # =========================================================
    # TOOL REGISTRY
    # =========================================================

    tool_registry = ToolRegistry()

    tool_execution_service = ToolExecutionService(
        registry=tool_registry,
    )

    # ---------------------------------------------------------
    # Patient tools
    # ---------------------------------------------------------

    register_patient_tool = RegisterPatientTool(
        register_patient_use_case=register_patient_use_case,
    )

    find_patient_tool = FindPatientTool(
        find_patient_use_case=find_patient_use_case,
    )

    tool_registry.register_many(
        [
            register_patient_tool,
            find_patient_tool,
        ]
    )

    # =========================================================
    # APPLICATION USE CASES
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
    # PRESENTATION CONTROLLER
    # =========================================================

    controller = AIController(
        execute_ai_request=execute_ai_request,
        execute_tool_call=execute_tool_call,
        list_tools=list_tools,
        explain_tool=explain_tool,
        summarize_conversation=summarize_conversation,
        conversation_history=None,
        presenter=ai_response_presenter,
    )

    return {
        # Infrastructure
        "conversation_repository": conversation_repository,
        "conversation_service": conversation_service,
        "llm_service": llm_service,

        # Tools
        "tool_registry": tool_registry,
        "tool_execution_service": tool_execution_service,

        # Use cases
        "execute_ai_request": execute_ai_request,
        "execute_tool_call": execute_tool_call,
        "list_tools": list_tools,
        "explain_tool": explain_tool,
        "summarize_conversation": summarize_conversation,

        # Presenters
        "ai_response_presenter": ai_response_presenter,
        "conversation_presenter": conversation_presenter,
        "tool_presenter": tool_presenter,

        # Presentation
        "controller": controller,
    }
