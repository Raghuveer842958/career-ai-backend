# app.agent.interview_agent.py

from ai.factories.llm_factory import get_llm
from pydantic import BaseModel
from typing import List
from ai.prompts.interview_prompts import (
    QUESTION_PROMPT,
    EVALUATION_PROMPT,
    REPORT_PROMPT
)

class QuestionResponse(BaseModel):
    question: str

class EvaluationResponse(BaseModel):
    score: int
    feedback: str
    strengths: List[str]
    weaknesses: List[str]

class ReportResponse(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]
    summary: str


llm = get_llm()

structured_llm = llm.with_structured_output(
    QuestionResponse
)


class InterviewAgent:

    def generate_question(
        self,
        jd,
        interview_type,
        difficulty,
        previous_questions,
        previous_answers
    ):
        
        question_llm = llm.with_structured_output(
            QuestionResponse
        )

        prompt = QUESTION_PROMPT.format(
            jd=jd,
            interview_type=interview_type,
            difficulty=difficulty,
            previous_questions=previous_questions,
            previous_answers=previous_answers,
        )

        response = structured_llm.invoke(prompt)

        return response.question


    def evaluate_answer(
        self,
        question,
        answer
    ):

        structured_llm = llm.with_structured_output(
            EvaluationResponse
        )

        prompt = EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
        )

        return structured_llm.invoke(prompt)


    def generate_report(
        self,
        questions,
        answers,
        scores,
        feedbacks
    ):

        structured_llm = llm.with_structured_output(
            ReportResponse
        )

        prompt = REPORT_PROMPT.format(
            questions=questions,
            answers=answers,
            scores=scores,
            feedbacks=feedbacks
        )

        return structured_llm.invoke(prompt)