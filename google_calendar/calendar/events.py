import datetime
from googleapiclient.errors import HttpError

from .utils import get_calendar_id

def create_event(
	service,
	cfg,
	calendar_id,
	title,
	start_datetime,
	end_datetime,
	location="",
	description="",
	color_id="",
	recurrence=None
) -> None:
	"""
	Create a single Google Calendar event.

	Args
		service: Google Calendar service
		cfg: calendar configurations
		calendar_id: ID of calendar to create the event in
		title: title of event
		start_datetime: start time of event
		end_datetime: end time of event
		location="": location of event
		description="": description of event
		recurrence: rule for recurrence of event, or None for one-time event
	"""
	event_body = {
		"summary": title,
		"location": location,
		"description": description,
		"start": {"dateTime": start_datetime.isoformat(), "timeZone": cfg.timezone},
		"end": {"dateTime": end_datetime.isoformat(), "timeZone": cfg.timezone},
	}

	if recurrence:
		event_body["recurrence"] = recurrence
		event_body["colorId"] = color_id

	try:
		event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
		print(f"Created event: {event.get('summary')} on {start_datetime}")
		return event
	except HttpError as error:
		print(f"Google API Error - create event: {error}")
		return None

def create_term_class_events(
	service,
	cfg,
	calendar_key,
	title,
	day_of_week,
	start_time,
	end_time,
	location="",
	description=""
):
	"""
	Create a recurring weekly class for the term using RRULE, skipping BREAK_WEEKS.

	Args
		service: Google Calendar service
		calendar_key: name of calendar to create the event in
		day_of_week: day of week of event
		title: title of event
		start_time: start time of event
		end_time: end time of event
		location="": location of event
		description="": description of event
	"""

	tz = cfg.tz
	calendar_id = get_calendar_id(cfg, calendar_key)

	# Start date for week 1
	class_date = cfg.term_start_monday + datetime.timedelta(days=day_of_week)
	start_dt = tz.localize(datetime.datetime.combine(class_date, start_time))
	end_dt = tz.localize(datetime.datetime.combine(class_date, end_time))

	# RRULE: weekly recurrence
	rrule = f"RRULE:FREQ=WEEKLY;COUNT={cfg.term_weeks}"

	# EXDATEs for skipped weeks
	exdates = []
	for week in cfg.break_weeks:
		delta_days = (week - 1) * 7 + day_of_week
		skip_date = cfg.term_start_monday + datetime.timedelta(days=delta_days)
		ex_dt = tz.localize(datetime.datetime.combine(skip_date, start_time))
		exdates.append(ex_dt.strftime("%Y%m%dT%H%M%S"))

	recurrence = [rrule]
	if exdates:
		recurrence.extend([f"EXDATE;TZID={cfg.timezone}:{d}" for d in exdates])

	create_event(
		service=service,
		cfg=cfg,
		calendar_id=calendar_id,
		title=title,
		start_datetime=start_dt,
		end_datetime=end_dt,
		location=location,
		description=description,
		color_id=cfg.recurrence_color_id,
		recurrence=recurrence
	)

def read_events_for_week(service, cfg, calendar_id, week_start):
	"""
	Read all events from Monday to end of Sunday of the same week week_start
	"""

	tz = cfg.tz
	start_dt = datetime.datetime.combine(week_start, datetime.time.min).replace(tzinfo=tz)
	end_dt = datetime.datetime.combine(week_start + datetime.timedelta(days=6),
									   datetime.time.max).replace(tzinfo=tz)
	
	events_result = service.events().list(
		calendarId=calendar_id,
		timeMin=start_dt.isoformat(),
		timeMax=end_dt.isoformat(),
		singleEvents=True,
		orderBy="startTime"
	).execute()

	return events_result.get("items", [])
