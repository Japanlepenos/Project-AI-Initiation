from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    elevenlabs,
    silero
)

from CalendarTools import Calendar

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        tts = elevenlabs.TTS(voice_id="cgSgspJ2msm6clMCkdW9") # for different voices, get API voice IDs from https://api.elevenlabs.io/v1/voices
        silero_vad = silero.VAD.load()
        self.calendar = Calendar()

        super().__init__(
            instructions="""
                You are my personal assistant. Keep answers short, concise, casual and easy to understand. Remember that my name is Japan.
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