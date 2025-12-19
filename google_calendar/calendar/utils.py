def print_events(events):
	if not events:
		print("No upcoming events found.")
		return

	for event in events:
		start = event["start"].get("dateTime", event["start"].get("date"))
		print(start, event["summary"])