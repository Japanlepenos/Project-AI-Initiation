from __future__ import annotations
from typing import Any
from datetime import datetime, timezone
from googleapiclient.discovery import build
from livekit.agents import function_tool, RunContext
import GoogleAPI
from APICredentials import Credentials

class Calendar():
    def __init__(self):
        self.service = build("calendar", "v3", credentials=Credentials.getCredentials(creds: None))

    def get_upcoming_events(self):
        now = datetime.now(timezone.utc).isoformat()
        print("Getting upcoming events...")

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        
        return events



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