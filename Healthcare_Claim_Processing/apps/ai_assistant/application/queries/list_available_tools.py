from dataclasses import dataclass


@dataclass(frozen=True)
class ListAvailableToolsQuery:
    """
    Retrieve all registered tools.
    """
    pass