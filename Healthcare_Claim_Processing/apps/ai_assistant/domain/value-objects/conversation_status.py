from enum import Enum


class ConversationStatus(str, Enum):

    ACTIVE = "active"

    COMPLETED = "completed"

    ARCHIVED = "archived"