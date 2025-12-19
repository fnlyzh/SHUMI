import datetime
from googleapiclient.errors import HttpError
import pytz

from ..config_personal import CALENDARS, TERM_START_MONDAY, TERM_WEEKS, BREAK_WEEKS, TIMEZONE

def create_event(
	service,
	calendar_id,
	title,
	start_datetime,
	end_datetime,
	location="",
	description="",
	recurrence=None
) -> None:
	"""
	Create a single Google Calendar event.

	Args
		service: Google Calendar service
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
		"start": {"dateTime": start_datetime.isoformat(), "timeZone": TIMEZONE},
		"end": {"dateTime": end_datetime.isoformat(), "timeZone": TIMEZONE},
	}

	if recurrence:
		event_body["recurrence"] = recurrence

	try:
		event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
		print(f"Created event: {event.get('summary')} on {start_datetime}")
		return event
	except HttpError as error:
		print(f"Google API Error - create event: {error}")
		return None

def create_term_class_events(
	service,
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
	
	tz = pytz.timezone(TIMEZONE)
	calendar_id = CALENDARS.get(calendar_key)
	if not calendar_id:
		raise ValueError(f"Calendar key '{calendar_key}' not found in config")

	# Start date for week 1
	class_date = TERM_START_MONDAY + datetime.timedelta(days=day_of_week)
	start_dt = tz.localize(datetime.datetime.combine(class_date, start_time))
	end_dt = tz.localize(datetime.datetime.combine(class_date, end_time))

	# RRULE: weekly recurrence
	rrule = f"RRULE:FREQ=WEEKLY;COUNT={TERM_WEEKS}"

	# EXDATEs for skipped weeks
	exdates = []
	for week in BREAK_WEEKS:
		delta_days = (week - 1) * 7 + day_of_week
		skip_date = TERM_START_MONDAY + datetime.timedelta(days=delta_days)
		ex_dt = tz.localize(datetime.datetime.combine(skip_date, start_time))
		exdates.append(ex_dt.strftime("%Y%m%dT%H%M%S"))

	recurrence = [rrule]
	if exdates:
		recurrence.extend([f"EXDATE;TZID={TIMEZONE}:{d}" for d in exdates])

	create_event(
		service=service,
		calendar_id=calendar_id,
		title=title,
		start_datetime=start_dt,
		end_datetime=end_dt,
		location=location,
		description=description,
		recurrence=recurrence
	)
