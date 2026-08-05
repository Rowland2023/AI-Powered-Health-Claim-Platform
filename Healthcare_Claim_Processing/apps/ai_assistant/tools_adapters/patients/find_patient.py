from .tool import Tool, ToolParameter


class FindPatientTool(Tool):
    """
    Finds a patient using supported search criteria.
    """

    @property
    def name(self):
        return "find_patient"

    @property
    def description(self):
        return "Find an existing patient."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "patient_identifier",
                "string",
                "Patient ID, National ID, Email, or Phone Number"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError