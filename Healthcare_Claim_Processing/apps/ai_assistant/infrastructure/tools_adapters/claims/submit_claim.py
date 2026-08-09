from .tool import Tool, ToolParameter


class RegisterClaimTool(Tool):

    @property
    def name(self):
        return "register_claim"

    @property
    def description(self):
        return (
            "Register a previously created claim."
        )

    @property
    def parameters(self):

        return [

            ToolParameter(
                "claim_id",
                "uuid",
                "Claim identifier"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError