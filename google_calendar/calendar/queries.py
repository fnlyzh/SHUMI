import datetime

from googleapiclient.errors import HttpError

def read_upcoming_events(service, cfg, calendar_key, max_results=10):
	calendar_id = cfg.calendars[calendar_key]
	now = datetime.datetime.now(tz=cfg.tz).isoformat()

	try:
		events_result = (
			service.events()
			.list(
				calendarId=calendar_id,
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
		return []