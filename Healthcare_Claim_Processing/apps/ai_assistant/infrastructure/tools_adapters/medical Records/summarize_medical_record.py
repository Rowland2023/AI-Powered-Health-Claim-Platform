from .tool import Tool


class SummarizeMedicalRecordTool(Tool):

    @property
    def name(self):
        return "summarize_medical_record"

    @property
    def description(self):
        return "Summarize a patient's medical record."

    @property
    def parameters(self):

        return []

    def execute(self, **kwargs):

        raise NotImplementedError