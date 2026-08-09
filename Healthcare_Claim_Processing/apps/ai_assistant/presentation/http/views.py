from __future__ import annotations

import json
from json import JSONDecodeError
from uuid import UUID

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from ai_assistant.presentation.http.controllers.ai_assistant import (
    AIController,
)

from ai_assistant.presentation.http.serializers.ai_request_serializer import (
    AIRequestSerializer,
)

from ai_assistant.presentation.http.serializers.tool_call_serializer import (
    ToolCallSerializer,
)


def _parse_json_body(request) -> dict:
    """
    Parse the Django request body as JSON.
    """

    try:
        return json.loads(
            request.body.decode("utf-8")
        )

    except (JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(
            "Request body must contain valid JSON."
        ) from exc


def _validation_error(
    error: ValidationError,
) -> JsonResponse:
    """
    Convert Pydantic validation errors into
    an HTTP 400 response.
    """

    return JsonResponse(
        {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": error.errors(),
            },
        },
        status=400,
    )


def create_ai_views(
    controller: AIController,
):
    """
    Create Django HTTP views for the AI Assistant
    bounded context.

    The views contain only HTTP concerns.

    They do not:
        - execute business rules
        - access repositories
        - manage transactions
        - access PostgreSQL
        - call infrastructure services directly
    """

    # =========================================================
    # CHAT
    # =========================================================

    @require_http_methods(["POST"])
    async def chat(request):

        try:
            payload = _parse_json_body(request)

            serializer = AIRequestSerializer.model_validate(
                payload
            )

        except ValueError as exc:
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_JSON",
                        "message": str(exc),
                    },
                },
                status=400,
            )

        except ValidationError as exc:
            return _validation_error(exc)

        user_id_header = request.headers.get(
            "X-User-ID"
        )

        if not user_id_header:
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "MISSING_USER_ID",
                        "message": (
                            "X-User-ID header is required."
                        ),
                    },
                },
                status=400,
            )

        try:
            user_id = UUID(user_id_header)

        except ValueError:
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_USER_ID",
                        "message": (
                            "X-User-ID must be a valid UUID."
                        ),
                    },
                },
                status=400,
            )

        result = await controller.chat(
            serializer=serializer,
            user_id=user_id,
        )

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # EXECUTE TOOL
    # =========================================================

    @require_http_methods(["POST"])
    async def execute_tool(request):

        try:
            payload = _parse_json_body(request)

            serializer = ToolCallSerializer.model_validate(
                payload
            )

        except ValueError as exc:
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_JSON",
                        "message": str(exc),
                    },
                },
                status=400,
            )

        except ValidationError as exc:
            return _validation_error(exc)

        result = await controller.execute_tool(
            serializer
        )

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # LIST AVAILABLE TOOLS
    # =========================================================

    @require_http_methods(["GET"])
    async def list_tools(request):

        result = await controller.list_tools()

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # EXPLAIN TOOL
    # =========================================================

    @require_http_methods(["GET"])
    async def explain_tool(
        request,
        tool_name: str,
    ):

        result = await controller.explain_tool(
            tool_name
        )

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # CONVERSATION HISTORY
    # =========================================================

    @require_http_methods(["GET"])
    async def history(
        request,
        conversation_id: UUID,
    ):

        result = await controller.history(
            conversation_id
        )

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # SUMMARIZE CONVERSATION
    # =========================================================

    @require_http_methods(["POST"])
    async def summarize(
        request,
        conversation_id: UUID,
    ):

        result = await controller.summarize(
            conversation_id
        )

        return JsonResponse(
            result,
            status=200,
        )

    # =========================================================
    # RETURN VIEW FUNCTIONS
    # =========================================================

    return {
        "chat": chat,
        "execute_tool": execute_tool,
        "list_tools": list_tools,
        "explain_tool": explain_tool,
        "history": history,
        "summarize": summarize,
    }