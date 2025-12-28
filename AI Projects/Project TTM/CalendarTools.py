from datetime import datetime, timezone
from livekit.agents import Agent, function_tool, RunContext
from CalendarAPI import CalendarAPI

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
        Retrieve the event details focusing on the event name, time & date, location and invitees. Infer the name of attendees from email addresses.

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

if __name__ == "__main__":
    userCalendar = Calendar()
    upcomingEvents = userCalendar.getUpcomingEvents(None, 10)

    print(type(upcomingEvents))
    print(upcomingEvents)

# events_result = (
#     self.schedule.events()
#     .list(
#         calendarId="primary",
#         timeMin=now,
#         maxResults=10,
#         singleEvents=True,
#         orderBy="startTime",
#     )
#     .execute()
# )
    
# @function_tool()
# async def lookup_drug_info(context: RunContext, drug_name: str) -> dict[str, Any]:
#     """Look up basic drug information for a medication.

#     Use this when the user asks what a drug is, what it treats, or common side effects.
#     Args:
#       drug_name: Name of the medication (generic or brand).
#     Returns:
#       A JSON object with short, patient-friendly facts.
#     """
#     # TODO: call your external API here
#     # For now: stub
#     return {
#         "drug": drug_name,
#         "uses": ["example use 1", "example use 2"],
#         "common_side_effects": ["nausea", "dizziness"],
#         "warnings": ["seek medical advice for severe symptoms"],
#     }