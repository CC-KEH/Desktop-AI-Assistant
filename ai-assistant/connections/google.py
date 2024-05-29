from asyncio import events
import os
import os.path
import datetime as dt 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class Google:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/calendar"]
        self.creds = None
        self.folder_id = None
        self.backup_path = "data/backup/"

    def get_credentials(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "token.json", self.scopes
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def connect_drive(self):
        try:
            self.get_credentials()
            self.service = build("drive", "v3", credentials=self.creds)
            response = (
                self.service.files()
                .list(
                    q="name='BackupFolder2024' and mimeType='application/vnd.google-apps.folder'",
                    spaces="drive",
                )
                .execute()
            )
            if not response["files"]:
                file_metadata = {
                    "name": "BackupFolder2024",
                    "mimeType": "application/vnd.google-apps.folder",
                }
                file = (
                    self.service.files()
                    .create(body=file_metadata, fields="id")
                    .execute()
                )
                print("Folder created successfully!")
                self.folder_id = file.get("id")
            else:
                self.folder_id = response["files"][0].get("id")
                print("Folder already exists!")
        except HttpError as error:
            print(f"error while establishing connection with google drive: {error}")

    def upload_files(self):
        try:
            for file in os.listdir(self.backup_path):
                file_metadata = {"name": file, "parents": [self.folder_id]}
                media = MediaFileUpload(self.backup_path + file)
                self.service.files().create(
                    body=file_metadata, media_body=media, fields="id"
                ).execute()
                print(f"{file} backed up")
                os.remove(self.backup_path + file)
        except HttpError as error:
            print(f"error while uploading files to google drive: {error}")

    def connect_calendar(self):
        try:
            self.calendar_service = build("calendar", "v3", credentials=self.creds)
            now = dt.datetime.now().isoformat() + "Z"
            event_result = self.calendar_service.events().list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()
            events = event_result.get("items", [])
            if not events:
                print("No upcoming events found.")
                return
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
            
        except HttpError as error:
            print(f"error while establishing connection with google calendar: {error}")
    
    def create_event(self,start_datetime,end_datetime,summary,description,location):
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "colorId": 7,
            "start": {"dateTime": start_datetime, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_datetime, "timeZone": "Asia/Kolkata"},
            "reminders": {"useDefault": False, "overrides": [{"method": "email", "minutes": 24 * 60}]},
        }
        try:
            event = self.calendar_service.events().insert(calendarId="primary", body=event).execute()
            print(f"Event created: {(event.get("htmlLink"))}")
        except HttpError as error:
            print(f"error while creating event in google calendar: {error}")
            
if __name__ == "__main__":
    google = Google()
    google.connect_drive()
    google.upload_files()
    google.connect_calendar()
    google.create_event(start_datetime="2024-01-01T09:00:00",
                        end_datetime="2024-01-01T10:00:00",
                        summary="AI Assistant Meeting",
                        description="Meeting with AI Assistant",
                        location="Virtual")