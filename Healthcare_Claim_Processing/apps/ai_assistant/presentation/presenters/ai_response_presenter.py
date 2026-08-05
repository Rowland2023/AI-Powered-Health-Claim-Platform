from __future__ import annotations

from shared.application.dto.result import Result


class AIResponsePresenter:
    """
    Converts Application Results into HTTP responses.
    """

    @staticmethod
    def present(result: Result) -> dict:

        if result.is_failure:

            return {
                "success": False,
                "error": {
                    "code": result.error.code,
                    "message": result.error.message,
                },
            }

        return {
            "success": True,
            "data": result.value,
        }