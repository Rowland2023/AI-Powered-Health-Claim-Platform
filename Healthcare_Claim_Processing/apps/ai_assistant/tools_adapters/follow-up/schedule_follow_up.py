from .tool import Tool, ToolParameter


class ScheduleFollowUpTool(Tool):

    @property
    def name(self):
        return "schedule_follow_up"

    @property
    def description(self):
        return (
            "Schedule a follow-up appointment."
        )

    @property
    def parameters(self):

        return [

            ToolParameter(
                "patient_id",
                "uuid",
                "Patient identifier"
            ),

            ToolParameter(
                "appointment_date",
                "datetime",
                "Follow-up appointment date"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError