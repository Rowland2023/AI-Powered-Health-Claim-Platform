from .tool import Tool, ToolParameter


class UpdateMedicalRecordTool(Tool):
    """
    Updates an existing patient's medical record.
    """

    @property
    def name(self) -> str:
        return "update_medical_record"

    @property
    def description(self) -> str:
        return "Update an existing patient's medical record."

    @property
    def parameters(self):

        return [

            ToolParameter(
                "medical_record_id",
                "uuid",
                "Medical record identifier"
            ),

            ToolParameter(
                "diagnosis",
                "string",
                "Updated diagnosis"
            ),

            ToolParameter(
                "treatment_plan",
                "string",
                "Updated treatment plan",
                required=False
            )
        ]

    def execute(self, **kwargs):
        raise NotImplementedError