from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI, APIConnectionError, AuthenticationError, OpenAIError

#Load environment variables from .env file
load_dotenv()

#Sanity check if OpenAI key is loaded and works
try:
    client = OpenAI()            # reads OPENAI_API_KEY from env
    client.models.list()         # lightweight call
    print("✅ OpenAI client works (key loaded).")
except AuthenticationError:
    print("❌ Auth failed: key missing/invalid (check .env path/name).")
except APIConnectionError as e:
    print("🌐 Network issue (key may be fine):", e)
except OpenAIError as e:
    print("⚠️ OpenAI error:", e)

#Load OpenAI client and make a TTS request
client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input="Today is a wonderful day to build something people love!",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)