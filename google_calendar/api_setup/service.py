from googleapiclient.discovery import build

def get_calendar_service(creds):
    return build("calendar", "v3", credentials=creds)

def get_tasks_service(creds):
    return build("tasks", "v1", credentials=creds)