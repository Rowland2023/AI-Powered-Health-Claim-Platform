from datetime import datetime

from pydantic import BaseModel


class MessageSerializer(BaseModel):

    role: str

    content: str

    created_at: datetime