from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Dict, Any



class InterviewReportModel(BaseModel):
    user_id: str | None = None
    jd: str
    interview_type: str
    difficulty: str
    questions: List[str]
    answers: List[str]
    scores: List[int]
    rounds: List[Dict[str, Any]]
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]
    summary: str
    created_at: datetime


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