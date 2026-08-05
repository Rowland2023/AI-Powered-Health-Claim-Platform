from __future__ import annotations

from shared.application.dto.result import Result


class ConversationPresenter:

    @staticmethod
    def present(result: Result) -> dict:

        if result.is_failure:

            return {
                "success": False,
                "message": result.error.message,
            }

        conversation = result.value

        return {
            "success": True,
            "conversation": conversation,
        }