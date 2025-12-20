def get_calendar_id(cfg, calendar_key: str) -> str:
	try:
		return cfg.calendars[calendar_key]
	except KeyError:
		raise ValueError(f"Calendar key '{calendar_key}' not found in config")

def print_events(events):
	if not events:
		print("No upcoming events found.")
		return

	for event in events:
		start = event["start"].get("dateTime", event["start"].get("date"))
		print(start, event["summary"])