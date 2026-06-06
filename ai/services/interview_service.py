import uuid

from ai.memory.interview_memory import interview_sessions
from ai.agent.interview_agent import InterviewAgent
from app.database import interviews_collection
from datetime import datetime
from app.voice.tts_service import (
    text_to_speech
)


agent = InterviewAgent()


async def start_interview(config):

    session_id = str(uuid.uuid4())

    first_question = (
        agent.generate_question(
            jd=config.jd,
            interview_type=config.interview_type,
            difficulty=config.difficulty,
            previous_questions=[],
            previous_answers=[],
        )
    )

    audio_file = await text_to_speech(
        first_question
    )

    interview_sessions[session_id] = {

        "config":
            config.model_dump(),

        "questions":
            [first_question],

        "answers":
            [],

        "scores":
            [],

        "feedbacks":
            [],

        "interview_rounds":
            [],

        "current_question":
            first_question,

        "current_question_audio":
            audio_file,

        "started_at":
            datetime.utcnow(),

        "completed":
            False,

        "report":
            None,
    }

    return {

        "session_id":
            session_id,

        "question":
            first_question,

        "audio_file":
            audio_file,

        "question_number":
            1,

        "total_questions":
            config.total_questions,
    }



async def submit_answer(
    session_id: str,
    answer: str,
    answer_audio: str | None = None,
):

    session = interview_sessions.get(
        session_id
    )

    if not session:
        raise ValueError(
            "Invalid session id"
        )

    question = session[
        "current_question"
    ]

    evaluation = (
        agent.evaluate_answer(
            question=question,
            answer=answer,
        )
    )

    session["answers"].append(
        answer
    )

    session["scores"].append(
        evaluation.score
    )

    session["feedbacks"].append(
        evaluation.feedback
    )

    # Save Current Round
    session["interview_rounds"].append({

        "question":
            question,

        "question_audio":
            session[
                "current_question_audio"
            ],

        "answer":
            answer,

        "answer_audio":
            answer_audio,

        "score":
            evaluation.score,

        "feedback":
            evaluation.feedback,

        "strengths":
            evaluation.strengths,

        "weaknesses":
            evaluation.weaknesses,
    })

    total_questions = (
        session["config"][
            "total_questions"
        ]
    )

    asked_questions = len(
        session["questions"]
    )

    # Interview Complete
    if asked_questions >= total_questions:

        report = (
            agent.generate_report(
                questions=session[
                    "questions"
                ],
                answers=session[
                    "answers"
                ],
                scores=session[
                    "scores"
                ],
                feedbacks=session[
                    "feedbacks"
                ],
            )
        )

        report_data = (
            report.model_dump()
        )

        interview_doc = {

            "user_id":
                session["config"].get(
                    "user_id"
                ),

            "jd":
                session["config"]["jd"],

            "interview_type":
                session["config"][
                    "interview_type"
                ],

            "difficulty":
                session["config"][
                    "difficulty"
                ],

            "questions":
                session["questions"],

            "answers":
                session["answers"],

            "scores":
                session["scores"],

            "rounds":
                session[
                    "interview_rounds"
                ],

            "overall_score":
                report_data[
                    "overall_score"
                ],

            "strengths":
                report_data[
                    "strengths"
                ],

            "weaknesses":
                report_data[
                    "weaknesses"
                ],

            "improvements":
                report_data[
                    "improvements"
                ],

            "summary":
                report_data[
                    "summary"
                ],

            "created_at":
                datetime.utcnow(),
        }

        result = (
            await interviews_collection.insert_one(
                interview_doc
            )
        )

        report_data[
            "interview_id"
        ] = str(
            result.inserted_id
        )

        session["report"] = (
            report_data
        )

        session["completed"] = True

        return {
            "completed": True,
            "report": report_data,
        }

    # Generate Next Question
    next_question = (
        agent.generate_question(
            jd=session["config"]["jd"],

            interview_type=
                session["config"][
                    "interview_type"
                ],

            difficulty=
                session["config"][
                    "difficulty"
                ],

            previous_questions=
                session["questions"],

            previous_answers=
                session["answers"],
        )
    )

    audio_file = (
        await text_to_speech(
            next_question
        )
    )

    session["questions"].append(
        next_question
    )

    session["current_question"] = (
        next_question
    )

    session[
        "current_question_audio"
    ] = audio_file

    return {
        "completed": False,

        "question_number":
            len(
                session["questions"]
            ),

        "total_questions":
            session["config"][
                "total_questions"
            ],

        "question":
            next_question,

        "feedback":
            evaluation.feedback,

        "score":
            evaluation.score,

        "audio_file":
            audio_file,
    }