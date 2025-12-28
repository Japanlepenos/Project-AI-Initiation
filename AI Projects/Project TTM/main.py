from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    elevenlabs,
    silero
)

from tools.CalendarTools import Calendar

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        # tts = elevenlabs.TTS(voice_id="EXAVITQu4vr4xnSDxMaL") # for different voices, get API voice IDs from https://api.elevenlabs.io/v1/voices
        tts = openai.TTS(
            model="gpt-4o-mini-tts",
            voice="fable",
            instructions="Speak in a friendly, natural American accent. Crisp, warm, not robotic.",
        )
        silero_vad = silero.VAD.load()
        self.calendar = Calendar()

        super().__init__(
            instructions="""
                You are my personal assistant. Always keep answer short, unless explicitly asked for more details. Remember that my name is Japan.
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
            tools =[self.calendar.getUpcomingEvents],
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
        instructions="Hello. How can I help you today?",
    )

if __name__ == "__main__":
    agents.cli.run_app(server)