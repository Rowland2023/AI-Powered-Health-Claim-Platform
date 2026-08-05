from .tool import Tool, ToolParameter


class SendNotificationTool(Tool):
    """
    Sends a notification to a patient, provider, or staff member.
    """

    @property
    def name(self):
        return "send_notification"

    @property
    def description(self):
        return "Send a notification."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "recipient_id",
                "uuid",
                "Recipient identifier"
            ),

            ToolParameter(
                "channel",
                "string",
                "Notification channel (Email, SMS, Push)"
            ),

            ToolParameter(
                "message",
                "string",
                "Notification message"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError