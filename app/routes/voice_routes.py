from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from pydantic import BaseModel

import os
import uuid

from app.voice.tts_service import (
    text_to_speech
)

from app.voice.stt_service import (
    speech_to_text
)

router = APIRouter()


class TTSRequest(BaseModel):
    text: str


@router.post("/speak")
async def speak(
    request: TTSRequest
):

    file_name = await text_to_speech(
        request.text
    )

    return {
        "audio_file": file_name
    }


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...)
):

    os.makedirs(
        "temp",
        exist_ok=True
    )

    # temp_file = (
    #     f"temp/{uuid.uuid4()}.webm"
    # )

    audio_file_name = (
        f"{uuid.uuid4()}.webm"
    )

    temp_file = (
        f"backend/app/voice/user_audio/{audio_file_name}"
    )

    with open(
        temp_file,
        "wb"
    ) as f:

        content = await file.read()

        f.write(content)

    text = await speech_to_text(
        temp_file
    )

    return {
        "text": text,
        "audio_file": audio_file_name,
    }