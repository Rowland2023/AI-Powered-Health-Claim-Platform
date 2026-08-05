from .tool import Tool, ToolParameter


class CancelFollowUpTool(Tool):
    """
    Cancels a scheduled follow-up appointment.
    """

    @property
    def name(self):
        return "cancel_follow_up"

    @property
    def description(self):
        return "Cancel a scheduled follow-up appointment."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "appointment_id",
                "uuid",
                "Follow-up appointment identifier"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError