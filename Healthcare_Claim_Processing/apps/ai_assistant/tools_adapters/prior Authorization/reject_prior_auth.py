from .tool import Tool, ToolParameter


class RejectPriorAuthorizationTool(Tool):
    """
    Rejects a prior authorization request.
    """

    @property
    def name(self):
        return "reject_prior_authorization"

    @property
    def description(self):
        return "Reject a prior authorization request."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "prior_authorization_id",
                "uuid",
                "Prior authorization identifier"
            ),

            ToolParameter(
                "reason",
                "string",
                "Reason for rejection"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError