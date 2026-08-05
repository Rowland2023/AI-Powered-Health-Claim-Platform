import json

from ai_assistant.domain.entities.tool_call import ToolCall
from ai_assistant.domain.value_objects.tool_argument import ToolArgument
from ai_assistant.domain.value_objects.tool_name import ToolName
from ai_assistant.domain.value_objects.tool_result import ToolResult

from ..models.tool_call_model import ToolCallModel


class ToolCallMapper:

    @staticmethod
    def to_model(
        tool_call: ToolCall,
        conversation_id,
    ) -> ToolCallModel:

        arguments = json.dumps(
            {
                arg.name: arg.value
                for arg in tool_call.arguments
            }
        )

        result = None

        if tool_call.result:

            result = json.dumps(
                {
                    "success": tool_call.result.success,
                    "message": tool_call.result.message,
                    "data": tool_call.result.data,
                    "error": tool_call.result.error,
                }
            )

        return ToolCallModel(
            id=tool_call.id,
            conversation_id=conversation_id,
            tool_name=str(tool_call.tool_name),
            arguments_json=arguments,
            result_json=result,
            status=tool_call.status,
            created_at=tool_call.created_at,
            executed_at=tool_call.executed_at,
        )

    @staticmethod
    def to_domain(
        model: ToolCallModel,
    ) -> ToolCall:

        arguments = []

        payload = json.loads(model.arguments_json)

        for key, value in payload.items():

            arguments.append(
                ToolArgument(
                    key,
                    value,
                )
            )

        result = None

        if model.result_json:

            data = json.loads(model.result_json)

            result = ToolResult(
                success=data["success"],
                data=data["data"],
                message=data["message"],
                error=data["error"],
            )

        return ToolCall(
            id=model.id,
            tool_name=ToolName(model.tool_name),
            arguments=arguments,
            result=result,
            status=model.status,
            created_at=model.created_at,
            executed_at=model.executed_at,
        )