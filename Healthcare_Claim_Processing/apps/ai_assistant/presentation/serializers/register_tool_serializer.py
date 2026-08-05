from pydantic import BaseModel


class RegisterToolSerializer(BaseModel):
    """
    Registers a new AI Tool.
    """

    name: str

    description: str