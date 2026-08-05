from .tool import Tool, ToolParameter


class RegisterPatientTool(Tool):
    """
    Registers a new patient.
    """

    @property
    def name(self):
        return "register_patient"

    @property
    def description(self):
        return "Register a new patient."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "first_name",
                "string",
                "Patient first name"
            ),

            ToolParameter(
                "last_name",
                "string",
                "Patient last name"
            ),

            ToolParameter(
                "date_of_birth",
                "date",
                "Patient date of birth"
            ),

            ToolParameter(
                "gender",
                "string",
                "Patient gender"
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError