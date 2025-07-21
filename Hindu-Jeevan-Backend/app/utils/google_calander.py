from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    token_path = "app/token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("/Users/er.vishalmishra/Documents/Hindu-Jeevan-Backend/app/client_secret_697219570053-bvfmq2c75i7m0mvc9lr13nmqrbshpdlh.apps.googleusercontent.com.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service

def add_event_to_calendar(summary, description, start_datetime, duration_minutes=30):
    service = get_calendar_service()
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_datetime.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_datetime.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get("htmlLink")
