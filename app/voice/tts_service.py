import uuid
import edge_tts
import os

async def text_to_speech(
    text: str
):

    file_name = (
        f"{uuid.uuid4()}.mp3"
    )

    # output_path = (
    #     f"app/voice/generated_audio/{file_name}"
    # )

    output_dir = (
        "app/voice/generated_audio"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_path = os.path.join(
        output_dir,
        file_name
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(
        output_path
    )

    return file_name