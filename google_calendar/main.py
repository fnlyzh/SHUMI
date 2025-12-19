from .auth import get_credentials
from .service import get_calendar_service
from .calendar.queries import upcoming_events

def main():	
	creds = get_credentials()
	service = get_calendar_service(creds)

	print("Getting the upcoming 10 events")
	events = upcoming_events(service)

	if not events:
		print("No upcoming events found.")
		return

	for event in events:
		start = event["start"].get("dateTime", event["start"].get("date"))
		print(start, event["summary"])

if __name__ == "__main__":
	main()