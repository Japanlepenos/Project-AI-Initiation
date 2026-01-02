import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class CalendarAPI():
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/calendar"]

    def getCredentials(self):        
        # Token stores user access + refresh tokens
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        else:
            creds = None
        
        # If no valid credentials, login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        return creds

    def buildSchedule(self, creds):
        service = build("calendar", "v3", credentials=creds)
        return service
    
    def getEvents(self, schedule, startTime, maxResults):
        events_result = (
            schedule.events()
            .list(
                calendarId="primary",
                timeMin=startTime,
                maxResults=maxResults,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    
        return events_result