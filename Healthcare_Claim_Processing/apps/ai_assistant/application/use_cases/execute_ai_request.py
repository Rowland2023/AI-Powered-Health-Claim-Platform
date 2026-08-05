# ai_assistant/application/use_cases/execute_ai_request.py

from shared.application.result import Result

from ai_assistant.application.commands.execute_prompt import (
    ExecutePromptCommand,
)

from ai_assistant.application.dto.ai_response_dto import (
    AIResponseDTO,
)

from ai_assistant.application.services.llm_service import (
    LLMService,
)

from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)

from ai_assistant.application.services.conversation_service import (
    ConversationService,
)


class ExecuteAIRequestUseCase:

    def __init__(
        self,
        llm_service: LLMService,
        tool_execution_service: ToolExecutionService,
        conversation_service: ConversationService,
    ):
        self._llm = llm_service
        self._tools = tool_execution_service
        self._conversation = conversation_service

    async def execute(
        self,
        command: ExecutePromptCommand,
    ) -> Result[AIResponseDTO]:

        #
        # Load previous conversation
        #

        history = []

        if command.conversation_id:

            history = await self._conversation.get_history(
                command.conversation_id
            )

        #
        # Available tools
        #

        available_tools = self._tools.list_tools()

        #
        # Ask LLM which tools should be executed
        #

        tool_calls = await self._llm.generate_tool_calls(
            command=command,
            available_tools=available_tools,
            conversation_history=history,
        )

        tool_results = []

        #
        # Execute every tool
        #

        for tool_call in tool_calls:

            result = await self._tools.execute(
                tool_call.tool_name,
                tool_call.arguments,
            )

            tool_results.append(result)

        #
        # Generate final response
        #

        response = await self._llm.generate_final_response(
            prompt=command.prompt,
            tool_results=tool_results,
            conversation_history=history,
        )

        #
        # Save conversation
        #

        if command.conversation_id:

            await self._conversation.save_message(
                command.conversation_id,
                role="user",
                content=command.prompt,
            )

            await self._conversation.save_message(
                command.conversation_id,
                role="assistant",
                content=response.message,
            )

        return Result.success(response)