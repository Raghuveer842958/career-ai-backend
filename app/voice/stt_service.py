# from faster_whisper import (
#     WhisperModel
# )

# model = WhisperModel(
#     "tiny",
#     device="cpu",
#     compute_type="int8"
# )


# async def speech_to_text(
#     audio_path: str
# ):

#     segments, _ = model.transcribe(
#         audio_path
#     )

#     transcript = " ".join(
#         segment.text
#         for segment in segments
#     )

#     return transcript.strip()




from faster_whisper import WhisperModel

_model = None


def get_whisper_model():
    global _model

    if _model is None:
        _model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )

    return _model


async def speech_to_text(audio_path: str):

    model = get_whisper_model()

    segments, _ = model.transcribe(
        audio_path
    )

    transcript = " ".join(
        segment.text
        for segment in segments
    )

    return transcript.strip()