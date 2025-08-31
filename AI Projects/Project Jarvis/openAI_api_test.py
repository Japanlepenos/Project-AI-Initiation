from openai import OpenAI
from pathlib import Path
import os, sys 
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv(usecwd=True) 
load_dotenv(env_path, override=True)

############################################################
############################################################
############################################################
# Output connection to ChatGPT API connection

# Verify the variable exists and looks sane
key = os.getenv("OPENAI_API_KEY")
if not key:
    print("❌ OPENAI_API_KEY is missing after load_dotenv(). Check name & .env location.")
    sys.exit(1)

# Prove key is actually used by the SDK
try:
    client = OpenAI(api_key=key)
    print("✅ OpenAI client construction successful")
except Exception as e:
    print("❌ Could not construct OpenAI client:", repr(e))
    sys.exit(1)

# Test Request
try:
    r = client.responses.create(
        model="gpt-4o",
        input="Give me a fun fact"
    )
    print("✅ API call ok. Text:", r.output_text[:120])
except Exception as e:
    print("❌ API call failed:", repr(e))

############################################################
############################################################
############################################################
# GPT API inaction!

try:
    speech_file_path = Path(__file__).parent / "speech.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input="Today is a wonderful day to build something people love!",
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        response.stream_to_file(speech_file_path)

    print("✅ Response successfully received from API")
except Exception as e:
    print("❌ API call failed:", repr(e))
