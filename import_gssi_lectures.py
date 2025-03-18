import datetime
import json
import tqdm  # type: ignore
import os

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
GSSI_CALENDAR_ID = "gssi.it_2rr8fdrnt35v2r89sakau7tln4@group.calendar.google.com"
MY_SHORT_COURSES_MAP = {
    "HE-8": "Plasma physics around astrophysical compact objects",
    "HE-9": "Accretion power in astrophysical systems",
    "GC-1": "Feedback control and deep loop shaping",
    "GC-2": "Multi-messenger transient",
    "GC-3": "Nucleosynthesis",
    "GC-7": "Multi-probe Cosmology",
    "GC- 8": "Compact objects formation and evolution",
}
YEAR = 2025


def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def main():
    target_calendar_id = os.environ["TARGET_CALENDAR_ID"]
    creds = auth()
    service = build("calendar", "v3", credentials=creds)
    my_short_courses_events = []
    page_token = None
    while True:
        page = (
            service.events()
            .list(
                calendarId=GSSI_CALENDAR_ID,
                pageToken=page_token,
            )
            .execute()
        )
        for event in page["items"]:
            start_str = event.get("start", {}).get("dateTime", "")
            if not start_str:
                continue
            if datetime.datetime.fromisoformat(start_str).date().year != YEAR:
                continue
            summary = event.get("summary", "")
            summary_parts = summary.strip().split(" ")
            prefix = summary_parts[0]
            if not any(course_id == prefix for course_id in MY_SHORT_COURSES_MAP):
                continue
            new_summary = prefix + " " + MY_SHORT_COURSES_MAP[prefix]
            event["summary"] = new_summary
            my_short_courses_events.append(event)
        page_token = page.get("nextPageToken")
        if not page_token:
            break

    with open("dump.json", "w") as f:
        json.dump(my_short_courses_events, f, ensure_ascii=False, indent=2)

    for event in tqdm.tqdm(my_short_courses_events):
        event.pop("id", None)
        event.pop("organizer", None)
        service.events().import_(calendarId=target_calendar_id, body=event).execute()


if __name__ == "__main__":
    main()
