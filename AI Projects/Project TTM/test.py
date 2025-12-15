import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

print("Loaded .env from:", env_path)
print("API KEY present:", bool(os.getenv("OPENAI_API_KEY")))

# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Print the API key to verify it's being read correctly
print("API Key:", os.environ.get("OPENAI_API_KEY"))

resp = client.responses.create(
    input="Say 'API key works' in one short sentence."
)

print(resp.output_text)