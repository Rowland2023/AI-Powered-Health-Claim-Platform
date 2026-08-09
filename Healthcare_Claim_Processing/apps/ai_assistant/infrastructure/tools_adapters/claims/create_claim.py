from .tool import Tool, ToolParameter


class CreateClaimTool(Tool):

    @property
    def name(self) -> str:
        return "create_claim"

    @property
    def description(self) -> str:
        return (
            "Create a new health insurance claim."
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
                "provider_id",
                "uuid",
                "Healthcare provider identifier"
            ),

            ToolParameter(
                "diagnosis",
                "string",
                "Primary diagnosis"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError