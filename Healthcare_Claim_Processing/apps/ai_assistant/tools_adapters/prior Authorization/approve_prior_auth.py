from .tool import Tool, ToolParameter


class ApprovePriorAuthorizationTool(Tool):
    """
    Approves a prior authorization request.
    """

    @property
    def name(self):
        return "approve_prior_authorization"

    @property
    def description(self):
        return "Approve a prior authorization request."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "prior_authorization_id",
                "uuid",
                "Prior authorization identifier"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError