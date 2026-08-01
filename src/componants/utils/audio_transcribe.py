from groq import Groq
from openai import OpenAI


def transcribe_audio_groq(audio_bytes: bytes, api_key: str, filename: str = "input.wav") -> str:
    if not api_key:
        raise ValueError("A Groq API key is required to transcribe audio.")
    client = Groq(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-large-v3",
        response_format="text",
    )
    return transcription if isinstance(transcription, str) else transcription.text


def transcribe_audio_openai(audio_bytes: bytes, api_key: str, filename: str = "input.wav") -> str:
    if not api_key:
        raise ValueError("An OpenAI API key is required to transcribe audio.")
    client = OpenAI(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-1",
    )
    return transcription.text


def transcribe_audio(audio_bytes: bytes, provider: str, api_key: str, filename: str = "input.wav") -> str:
    """
    Dispatches to the right provider's transcription API based on
    whichever LLM the user has selected in the sidebar.
    """
    if provider == "Groq":
        return transcribe_audio_groq(audio_bytes, api_key, filename)
    elif provider == "OpenAI":
        return transcribe_audio_openai(audio_bytes, api_key, filename)
    raise ValueError(f"No transcription support for provider: {provider}")
