from app.database import interviews_collection
from bson import ObjectId


async def get_interview_history():

    interviews = await (
        interviews_collection
        .find()
        .sort("created_at", -1)
        .to_list(length=100)
    )

    for interview in interviews:

        interview["_id"] = str(
            interview["_id"]
        )

        if "created_at" in interview:
            interview["created_at"] = str(
                interview["created_at"]
            )

    return interviews



async def get_interview_by_id(
    interview_id: str
):

    interview = await (
        interviews_collection.find_one(
            {
                "_id":
                ObjectId(interview_id)
            }
        )
    )

    if not interview:
        return None

    interview["_id"] = str(
        interview["_id"]
    )

    if "created_at" in interview:

        interview["created_at"] = str(
            interview["created_at"]
        )

    BASE_URL = (
        "http://localhost:8000"
    )

    rounds = interview.get(
        "rounds",
        []
    )

    for round_data in rounds:

        if round_data.get(
            "question_audio"
        ):

            round_data[
                "question_audio_url"
            ] = (
                f"{BASE_URL}/audio/"
                f"{round_data['question_audio']}"
            )

        if round_data.get(
            "answer_audio"
        ):

            round_data[
                "answer_audio_url"
            ] = (
                f"{BASE_URL}/user-audio/"
                f"{round_data['answer_audio']}"
            )

    return interview