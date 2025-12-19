from googleapiclient.discovery import build

def get_calendar_service(creds):
    return build("calendar", "v3", credentials=creds)