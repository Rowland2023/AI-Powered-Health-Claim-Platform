from .tool import Tool, ToolParameter


class SubmitPriorAuthorizationTool(Tool):

    @property
    def name(self):
        return "submit_prior_authorization"

    @property
    def description(self):
        return (
            "Submit a prior authorization request "
            "to an insurance provider."
        )

    @property
    def parameters(self):

        return [

            ToolParameter(
                "claim_id",
                "uuid",
                "Claim identifier"
            ),

            ToolParameter(
                "insurance_provider",
                "string",
                "Insurance company"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError