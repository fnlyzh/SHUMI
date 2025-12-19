import datetime

from collections import defaultdict

from ..calendar.utils import get_calendar_id
from ..calendar.events import read_events_for_week

def _get_monday_for_week(cfg, week_offset=0):
	"""
	Returns the date of Monday for the week.
	week_offset=0 -> current week
	week_offset=-1 -> previous week
	"""
	now = datetime.datetime.now(cfg.tz)
	
	# Monday = 0
	monday = now - datetime.timedelta(days=now.weekday())
	target_monday = monday + datetime.timedelta(weeks=week_offset)
	
	return target_monday

def _total_time_per_course(events):
	"""
	Returns a dict: {course_title: total_hours}
	"""
	totals = defaultdict(float)
	for event in events:
		course_code = event.get("extendedProperties", {}).get("private", {}).get("subcategory")
		if course_code is None:
			continue

		start = event['start'].get('dateTime')
		end = event['end'].get('dateTime')
		if start is None or end is None:
			continue

		start_dt = datetime.datetime.fromisoformat(start)
		end_dt = datetime.datetime.fromisoformat(end)

		totals[course_code] += (end_dt - start_dt).total_seconds() / 3600

	return dict(totals)

def weekly_study_time(service, cfg, calendar_key, week_offset=0):
	"""
	Returns total hours spent per course for a specific week.
	week_offset=0 -> current week
	week_offset=-1 -> previous week
	"""
	calendar_id = get_calendar_id(cfg, calendar_key)

	week_start = _get_monday_for_week(cfg, week_offset)
	events = read_events_for_week(service, cfg, calendar_id, week_start)
	return _total_time_per_course(events)

# Convenience functions
def current_week(service, cfg, calendar_key="academic"):
	return weekly_study_time(service, cfg, calendar_key, week_offset=0)

def previous_week(service, cfg, calendar_key="academic", weeks_ago=1):
	return weekly_study_time(service, cfg, calendar_key, week_offset=-weeks_ago)