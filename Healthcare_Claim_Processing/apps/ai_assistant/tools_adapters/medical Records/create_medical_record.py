from .tool import Tool, ToolParameter


class CreateMedicalRecordTool(Tool):

    @property
    def name(self):
        return "create_medical_record"

    @property
    def description(self):
        return "Create a patient's medical record."

    @property
    def parameters(self):
        return [

            ToolParameter(
                "patient_id",
                "uuid",
                "Patient identifier"
            ),

            ToolParameter(
                "diagnosis",
                "string",
                "Medical diagnosis"
            )
        ]

    def execute(self, **kwargs):

        raise NotImplementedError