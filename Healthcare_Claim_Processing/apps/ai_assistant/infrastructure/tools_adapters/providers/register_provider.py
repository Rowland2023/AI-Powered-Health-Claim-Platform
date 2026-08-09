from .tool import Tool, ToolParameter


class RegisterProviderTool(Tool):
    """
    Registers a healthcare provider.
    """

    @property
    def name(self):
        return "register_provider"

    @property
    def description(self):
        return "Register a healthcare provider."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "provider_name",
                "string",
                "Healthcare provider name"
            ),

            ToolParameter(
                "license_number",
                "string",
                "Professional license number"
            ),

            ToolParameter(
                "specialization",
                "string",
                "Medical specialization"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError