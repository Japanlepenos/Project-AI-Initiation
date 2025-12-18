from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    elevenlabs,
    silero
)

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        # tts = elevenlabs.TTS()
        tts = elevenlabs.TTS(voice_id="FGY2WhTYpPnrIDTdsKH5") # for different voices, get API voice IDs from https://api.elevenlabs.io/v1/voices
        silero_vad = silero.VAD.load()

        super().__init__(
            instructions="""
                You are a doctor who is enthusiastic about helping patients. Keep answers short, concise, and easy to understand.
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
        )

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
        )
    )

    await session.generate_reply(
        instructions="Hello. I'm Baymax, your personal healthcare companion. How can I assist you today?",
    )

if __name__ == "__main__":
    agents.cli.run_app(server)