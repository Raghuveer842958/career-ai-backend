from fastapi import APIRouter
from pydantic import BaseModel

# from app.schemas.interview_schema import (
#     InterviewConfig,
#     AnswerRequest,
# )

from ai.services.interview_service import (
    start_interview,
    submit_answer,
)

from ai.memory.interview_memory import (
    interview_sessions
)

from ai.services.interview_history_service import (
    get_interview_history,
    get_interview_by_id
)

class InterviewConfig(BaseModel):
    jd: str
    resume: str | None = None
    interview_type: str
    difficulty: str
    total_questions: int


class AnswerRequest(BaseModel):
    session_id: str
    answer: str
    answer_audio: str | None = None

router = APIRouter()


@router.post("/start")
async def start(config: InterviewConfig):
    print("interview start route got called")
    return await start_interview(config)


@router.post("/answer")
async def answer(
    request: AnswerRequest
):
    return await submit_answer(
        session_id=request.session_id,
        answer=request.answer,
        answer_audio=request.answer_audio,
    )


@router.get("/report/{session_id}")
def get_report(
    session_id: str
):
    session = interview_sessions.get(
        session_id
    )

    if not session:
        return {
            "error": "Session not found"
        }

    return session.get("report")



@router.get("/history")
async def history():

    return await get_interview_history()


@router.get("/history/{interview_id}")
async def interview_details(
    interview_id: str
):
    return await get_interview_by_id(
        interview_id
    )