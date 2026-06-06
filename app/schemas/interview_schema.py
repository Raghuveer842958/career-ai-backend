from pydantic import BaseModel
from typing import List


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


class Evaluation(BaseModel):
    score: int
    feedback: str


class InterviewReport(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]