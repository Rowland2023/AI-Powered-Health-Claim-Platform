from __future__ import annotations

from django.urls import path

from ai_assistant.composition import create_ai_dependencies
from ai_assistant.presentation.http.views import (
    create_ai_views,
)


dependencies = create_ai_dependencies()

views = create_ai_views(
    dependencies["ai_controller"]
)


app_name = "ai_assistant"


urlpatterns = [
    path(
        "ai/chat/",
        views["chat"],
        name="chat",
    ),
    path(
        "ai/tools/",
        views["list_tools"],
        name="list-tools",
    ),
    path(
        "ai/tools/execute/",
        views["execute_tool"],
        name="execute-tool",
    ),
    path(
        "ai/tools/<str:tool_name>/",
        views["explain_tool"],
        name="explain-tool",
    ),
    path(
        "ai/conversations/<uuid:conversation_id>/history/",
        views["history"],
        name="conversation-history",
    ),
    path(
        "ai/conversations/<uuid:conversation_id>/summarize/",
        views["summarize"],
        name="summarize-conversation",
    ),
]