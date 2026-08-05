from .tool import Tool, ToolParameter


class ExplainClaimDenialTool(Tool):
    """
    Explains why a claim was denied.
    """

    @property
    def name(self):
        return "explain_claim_denial"

    @property
    def description(self):
        return "Explain why an insurance claim was denied."

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