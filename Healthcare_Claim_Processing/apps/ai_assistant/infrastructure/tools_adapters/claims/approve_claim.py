from .tool import Tool, ToolParameter


class ApproveClaimTool(Tool):

    @property
    def name(self):
        return "approve_claim"

    @property
    def description(self):
        return "Approve an insurance claim."

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