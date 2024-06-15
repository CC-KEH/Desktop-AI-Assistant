import os
import os.path
import datetime as dt
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from email.mime.text import MIMEText

from tools.utils import process_datetime

class Google:
    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send"
        ]
        self.creds = None
        self.folder_id = None
        self.backup_path = "saved_date/data/backup/"
        self.get_credentials()
        self.gmail_service = self.get_gmail_service()
        self.user_mail = "arbashhussain08@gmail.com"
    def get_credentials(self):
        if os.path.exists("connections/token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "connections/token.json", self.scopes
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "connections/credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open("connections/token.json", "w") as token:
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
            return True
        
        except HttpError as error:
            print(f"Error while establishing connection with google drive: {error}")
            return False
        
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
            return True
        except HttpError as error:
            print(f"Error while uploading files to google drive: {error}")
            return False
        
        
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
            return True
        except HttpError as error:
            print(f"Error while establishing connection with google calendar: {error}")
            return False
        
    def create_event(self,start_datetime,end_datetime,summary,location,description=""):
        self.calendar_service = build("calendar", "v3", credentials=self.creds)
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
            # print(f"Event created: {(event.get("htmlLink"))}")
            return True
        except HttpError as error:
            print(f"Error while creating event in google calendar: {error}")
            return False
        
    def get_gmail_service(self):
        return build('gmail', 'v1', credentials=self.creds)
    
    def get_mails(self):
        try:
            mails = []
            now = dt.datetime.now(dt.timezone.utc)
            yesterday = now - dt.timedelta(days=1)
            query = f"after:{int(yesterday.timestamp())}"
            results = self.gmail_service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            for message in messages:
                msg = self.gmail_service.users().messages().get(userId='me', id=message['id']).execute()
                msg_data = msg['payload']['headers']
                mail_from = ""
                mail_subject = ""
                for header in msg_data:
                    if header['name'] == 'Subject':
                        mail_subject = header['value']
                    if header['name'] == 'From':
                        mail_from = header['value']
                    if mail_from == self.user_mail:
                        mail_from = ""

                if mail_from=="" and mail_subject=="":
                    continue

                mails.append((mail_from, mail_subject))
            return mails
        except Exception as error:
            print("Error at get_mails: %s", error)
            return None
        
    def create_message(self,to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


    def send_mail(self, to, subject, message_text):
        message = self.create_message(to, subject, message_text)
        try:
            sent_message = self.gmail_service.users().messages().send(userId='me', body=message).execute()
            print(f"Message Id: {sent_message['id']}")
            return sent_message
        except Exception as error:
            print(f"Error occured while sending mail: {error}")
            return False
        
if __name__ == "__main__":
    google = Google()
    # google.connect_drive()
    # google.upload_files()
    # google.connect_calendar()
    start_datetime = process_datetime()
    end_datetime = process_datetime()
    google.create_event(start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        summary="Testing",
                        description="Testing mail and calendar event creation",
                        location="Virtual")
    print(google.get_mails())
    # google.send_mail(to="mailid",subject="testing",message_text="This is a test mail")