from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)
def voice_generator(text, gender: str, filename="voice.mp3"):
    if gender.upper() == "MALE":
        voiceid = "IES4nrmZdUBHByLBde0P"
    else:
        voiceid = "jAAHNNqlbAX9iWjJPEtE"

    audio_stream = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voiceid,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings={
            "stability": 0.8,
            "similarity_boost": 0.9,
            "style": 0.9,
            "speed": 0.8,
            "use_speaker_boost": True
        }
    )

    audio_bytes = b"".join(audio_stream)

    with open(filename, "wb") as f:
        f.write(audio_bytes)

    return filename
 
