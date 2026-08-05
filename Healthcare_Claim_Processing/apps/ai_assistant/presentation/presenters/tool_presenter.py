from __future__ import annotations

from shared.application.dto.result import Result


class ToolPresenter:

    @staticmethod
    def present(result: Result) -> dict:

        if result.is_failure:

            return {
                "success": False,
                "message": result.error.message,
            }

        return {
            "success": True,
            "tools": result.value,
        }