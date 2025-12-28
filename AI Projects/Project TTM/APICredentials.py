import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCredentials():
    def __init__(self):
        self.creds = None
        self.scopes = ["https://www.googleapis.com/auth/calendar"]

    def getCredentials(self):
        # Token stores user access + refresh tokens
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)

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
    
    def buildCalendar(self, creds):
        service = build("calendar", "v3", credentials=creds)
        return service
    
if __name__ == "__main__":
    auth = GoogleCredentials()
    creds = auth.getCredentials()

    print("✅ Credentials loaded")
    print("Access token:", creds.token)
    print("Refresh token:", creds.refresh_token)
    print("Expiry:", creds.expiry)