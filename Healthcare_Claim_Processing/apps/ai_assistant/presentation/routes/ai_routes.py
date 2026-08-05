from fastapi import APIRouter, Depends
from uuid import UUID

from ..controllers.ai_controller import AIController
from ..serializers.ai_request_serializer import AIRequestSerializer
from ..serializers.tool_call_serializer import ToolCallSerializer

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


@router.post("/chat")
async def chat(
    request: AIRequestSerializer,
    controller: AIController = Depends(),
):
    return await controller.chat(
        serializer=request,
        user_id=request.user_id,
    )


@router.post("/tools/execute")
async def execute_tool(
    request: ToolCallSerializer,
    controller: AIController = Depends(),
):
    return await controller.execute_tool(request)


@router.get("/tools")
async def list_tools(
    controller: AIController = Depends(),
):
    return await controller.list_tools()


@router.get("/tools/{tool_name}")
async def explain_tool(
    tool_name: str,
    controller: AIController = Depends(),
):
    return await controller.explain_tool(tool_name)


@router.get("/conversations/{conversation_id}")
async def history(
    conversation_id: UUID,
    controller: AIController = Depends(),
):
    return await controller.history(conversation_id)


@router.post("/conversations/{conversation_id}/summary")
async def summarize(
    conversation_id: UUID,
    controller: AIController = Depends(),
):
    return await controller.summarize(conversation_id)