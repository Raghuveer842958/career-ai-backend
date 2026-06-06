from ai.agent.agent import get_career_agent
from fastapi import APIRouter
from pydantic import BaseModel

from fastapi.responses import StreamingResponse
import json

from ai.agent.agent import get_career_agent


router = APIRouter()
agent = get_career_agent()

class ChatRequest(BaseModel):
    query: str


@router.get("/stream")
async def stream_chat(query: str):

    async def event_generator():

        async for event in agent.astream_events(
            {"input": query},
            version="v2"
        ):

            event_name = event.get("event")

            # Tool Start
            if event_name == "on_tool_start":

                yield f"data: {json.dumps({
                    'type': 'tool_start',
                    'tool': event['name']
                })}\n\n"

            # Tool End
            elif event_name == "on_tool_end":

                yield f"data: {json.dumps({
                    'type': 'tool_end',
                    'tool': event['name']
                })}\n\n"

            # Token Stream
            elif event_name == "on_chat_model_stream":

                chunk = (
                    event.get("data", {})
                    .get("chunk")
                )

                if (
                    chunk and
                    hasattr(chunk, "content") and
                    chunk.content
                ):
                    yield f"data: {json.dumps({
                        'type': 'token',
                        'content': chunk.content
                    })}\n\n"

        yield f"data: {json.dumps({'type':'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )



@router.post("/")
async def chat(request: ChatRequest):

    response = agent.invoke({
        "input": request.query
    })

    print("\n\n========== RESPONSE ==========")
    print(response)
    print("==============================\n\n")

    steps = []

    for action, observation in response.get(
        "intermediate_steps",
        []
    ):

        steps.append({
            "tool": action.tool,
            "observation": str(observation)
        })

    return {
        "response": response["output"],
        "steps": steps
    }