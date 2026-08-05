from .tool import Tool, ToolParameter


class RejectClaimTool(Tool):
    """
    Rejects an insurance claim.
    """

    @property
    def name(self):
        return "reject_claim"

    @property
    def description(self):
        return "Reject a submitted insurance claim."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "claim_id",
                "uuid",
                "Claim identifier"
            ),

            ToolParameter(
                "reason",
                "string",
                "Reason for rejection"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError