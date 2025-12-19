import datetime

from ..calendar.utils import get_calendar_id
from ..calendar.events import read_events_for_week

def _get_monday_for_week(week_offset=0):
	"""
	Returns the date of Monday for the week.
	week_offset=0 -> current week
	week_offset=-1 -> previous week
	"""
	today = datetime.date.today()
	
	# Monday = 0
	monday = today - datetime.timedelta(days=today.weekday())
	target_monday = monday + datetime.timedelta(weeks=week_offset)
	
	return target_monday

def _total_time_per_course(events):
	"""
	Returns a dict: {course_title: total_hours}
	"""
	totals = {}
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		end = event['end'].get('dateTime', event['end'].get('date'))

		# parse datetime strings
		start_dt = datetime.datetime.fromisoformat(start)
		end_dt = datetime.datetime.fromisoformat(end)

		duration = (end_dt - start_dt).total_seconds() / 3600  # in hours

		title = event.get("summary", "(unknown)")
		totals[title] = totals.get(title, 0) + duration

	return totals

def weekly_study_time(service, cfg, calendar_key, week_offset=0):
	"""
	Returns total hours spent per course for a specific week.
	week_offset=0 -> current week
	week_offset=-1 -> previous week
	"""
	calendar_id = get_calendar_id(cfg, calendar_key)

	week_start = _get_monday_for_week(week_offset)
	events = read_events_for_week(service, cfg, calendar_id, week_start)
	return _total_time_per_course(events)

# Convenience functions
def current_week(service, cfg, calendar_key="academic"):
	return weekly_study_time(service, cfg, calendar_key, week_offset=0)

def previous_week(service, cfg, calendar_key="academic", weeks_ago=1):
	return weekly_study_time(service, cfg, calendar_key, week_offset=-weeks_ago)