import datetime

from googleapiclient.errors import HttpError

def read_upcoming_events(service, max_results=10):
	now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

	try:
		events_result = (
			service.events()
			.list(
				calendarId="primary",
				timeMin=now,
				maxResults=max_results,
				singleEvents=True,
				orderBy="startTime",
			)
			.execute()
		)
		
		return events_result.get("items", [])
	
	except HttpError as error:
		print(f"Google API Error: {error}")