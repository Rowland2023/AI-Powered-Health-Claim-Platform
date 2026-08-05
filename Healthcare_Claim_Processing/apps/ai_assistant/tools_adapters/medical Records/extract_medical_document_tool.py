from .tool import Tool


class ExtractMedicalDocumentTool(Tool):

    @property
    def name(self):
        return "extract_medical_document"

    @property
    def description(self):
        return (
            "Extract structured medical data "
            "from uploaded documents."
        )

    @property
    def parameters(self):

        return []

    def execute(self, **kwargs):

        raise NotImplementedError