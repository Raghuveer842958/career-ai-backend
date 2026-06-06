from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):

    name: str
    email: EmailStr
    age: int

class Job(BaseModel):
    job_id: str
    job_title: str
    employer_name: str
    employer_logo: str
    employer_website: str
    job_apply_link: str


class EvaluationResponse(BaseModel):
    score: int
    feedback: str


class ReportResponse(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]