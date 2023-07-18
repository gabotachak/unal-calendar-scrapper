from datetime import date
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from unal_calendar_scrapper.entities import UnalEvent

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TOKEN_PATH = os.path.join(ROOT_DIR, "token.json")
CREDENTIAL_PATH = os.path.join(ROOT_DIR, "credentials.json")

TIME_ZONE = "America/Bogota"
UNAL_LOCATION = "Universidad Nacional de Colombia, Cra 45, Bogotá, Colombia"


class GoogleCalendarClient:
    service = None

    def __init__(self) -> None:
        creds = None

        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIAL_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=creds)
        except HttpError as e:
            print("An error occurred: %s" % e)
            raise e

    def get_calendar_by_summary(self, summary: str) -> dict:
        calendars = self.service.calendarList().list().execute()
        calendars = calendars.get("items", [])

        summary = summary.lower()
        calendars = [c for c in calendars if summary == c["summary"].lower()]

        return calendars[0] if calendars else None

    def create_calendar(self, calendar_name: str) -> dict:
        calendar = {
            "summary": calendar_name,
            "timeZone": TIME_ZONE,
        }

        created_calendar = self.service.calendars().insert(body=calendar).execute()
        return created_calendar

    def get_events_by_calendar_id(self, calendar_id: str) -> list:
        events = self.service.events().list(calendarId=calendar_id).execute()
        events = events.get("items", [])

        return events

    def create_event(self, calendar_id: str, event: UnalEvent) -> dict:
        body = {
            "summary": event.activity,
            "location": UNAL_LOCATION,
            "description": f"Responsable: {event.description}",
            "start": {
                "date": str(event.start_date),
                "timeZone": TIME_ZONE,
            },
            "end": {
                "date": str(event.end_date),
                "timeZone": TIME_ZONE,
            },
        }

        try:
            event = (
                self.service.events()
                .insert(calendarId=calendar_id, body=body)
                .execute()
            )
        except HttpError as e:
            print("An error occurred: %s" % e)
            return None

        return event
