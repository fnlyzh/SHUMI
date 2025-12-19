import os
from dotenv import load_dotenv
load_dotenv()

import datetime

from .auth import get_credentials
from .service import get_calendar_service, get_tasks_service

from .calendar.queries import read_upcoming_events
from .calendar.events import create_term_class_events, create_event
from .calendar.utils import print_events
from .analytics.study_time import current_week, previous_week

from .tasks.queries import read_upcoming_tasks
from .tasks.utils import print_tasks

from .settings import CalendarConfig

# Calender API return object source:
# https://developers.google.com/workspace/calendar/api/v3/reference/events

# Tasks API return object source:
# https://developers.google.com/tasks/reference/rest/v1/tasks

def main():
	cfg_path = os.getenv("GCAL_CONFIG_PATH")
	if cfg_path is None:
		raise RuntimeError("GCAL_CONFIG_PATH is not set in .env")
	cfg = CalendarConfig.from_json(cfg_path)

	creds = get_credentials()
	calendar_service = get_calendar_service(creds)
	tasks_service = get_tasks_service(creds)

	# print("Upcoming Calendar Events")
	# events = read_upcoming_events(calendar_service, cfg=cfg, calendar_key="personal")
	# print_events(events)

	# print("Upcoming Tasks")
	# tasks = read_upcoming_tasks(tasks_service)
	# print_tasks(tasks, fields=["title", "due", "notes"])

	# create_term_class_events(
	# 	calendar_service, cfg, calendar_key="academic", title="COMP9999 Lecture 1",
	# 	day_of_week=1, start_time=datetime.time(9,0), end_time=datetime.time(11,0),
	# 	location="Building A, Room 101", description="epic lecture")

	print("Current week study times (hours):", current_week(calendar_service, cfg))
	print("Previous week study times (hours):", previous_week(calendar_service, cfg, weeks_ago=2))

	

if __name__ == "__main__":
	main()