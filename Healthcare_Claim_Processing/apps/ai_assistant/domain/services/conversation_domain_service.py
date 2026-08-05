from ..entities.conversation import Conversation
from ..entities.tool_call import ToolCall


class ConversationDomainService:
    """
    Domain logic involving Conversation behavior that doesn't
    naturally belong on a single Entity.
    """

    def request_tool(
        self,
        conversation: Conversation,
        tool_call: ToolCall,
    ) -> None:
        """
        Attach a ToolCall to the conversation.
        """

        conversation.add_tool_call(tool_call)

    def complete_tool(
        self,
        tool_call: ToolCall,
        result,
    ) -> None:
        """
        Mark a ToolCall as completed.
        """

        tool_call.complete(result)