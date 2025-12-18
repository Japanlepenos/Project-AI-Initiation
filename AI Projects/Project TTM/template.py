# Step 1: Import necessary modules and load environment variables
import logging

from dotenv import load_dotenv
_ = load_dotenv(override=True)

logger = logging.getLogger("dlai-agent")
logger.setLevel(logging.INFO)

from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext
from livekit.plugins import (
    openai,
    elevenlabs,
    silero,
)

# Step 2: Define the Assistant class
class Assistant(Agent):
    def __init__(self) -> None:
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        tts = elevenlabs.TTS()
        #tts = elevenlabs.TTS(voice_id="CwhRBWXzGAHq8TQ4Fs17")  # example with defined voice
        silero_vad = silero.VAD.load()

        super().__init__(
            instructions="""
                You are a helpful assistant communicating 
                via voice
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
        )

#Step 3: Create Entry Point
async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=Assistant()
    )