from datetime import datetime, timezone
from livekit.agents import Agent, function_tool, RunContext
from tools.CalendarAPI import CalendarAPI

class Calendar():
    def __init__(self):
        self.userCalendar = CalendarAPI()
        self.credentials = self.userCalendar.getCredentials()
        self.schedule = self.userCalendar.buildSchedule(self.credentials)

    @function_tool()
    async def getUpcomingEvents(self, ctx: RunContext, maxResults: int) -> dict:
        """
        Context for Agent:
        Fetches the upcoming calendar events from personal calendar. The maxResults parameter specifies how many events to retrieve.
        Always retrieve only the event name and time first. Do not give too much details unless requested.

        Args:
          maxResults: The maximum number of upcoming events to retrieve.

        Returns:
          A dictionary containing the upcoming events or a message indicating no events are found.

        """
        now = datetime.now(timezone.utc).isoformat()
        print("Getting upcoming events...")

        events_result = self.userCalendar.getEvents(
            self.schedule,
            startTime=now,
            maxResults=maxResults,
        )

        events = self.checkEmptyEvents(events_result, "No upcoming events found.")
        return events

    def checkEmptyEvents(self, events, no_event_message):
        if not events:
            return {"NoEventMessage": no_event_message}
        else:
            return events