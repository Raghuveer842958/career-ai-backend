from faster_whisper import (
    WhisperModel
)

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


async def speech_to_text(
    audio_path: str
):

    segments, _ = model.transcribe(
        audio_path
    )

    transcript = " ".join(
        segment.text
        for segment in segments
    )

    return transcript.strip()