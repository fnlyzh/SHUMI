import datetime

from .api_setup.auth import get_credentials
from .api_setup.service import get_calendar_service, get_tasks_service

from .calendar.events import create_term_class_events, create_event, read_upcoming_events
from .calendar.utils import print_events
from .analytics.study_time import current_week, previous_week

from .tasks.tasks import read_upcoming_tasks, read_tasklist_id, create_week_tasks, create_weekly_tasks
from .tasks.utils import print_tasks

from config.handler import load_calendar_config, load_tasks_config, load_discord_config

from .gcal_integration import flush_sessions_to_calendar

# Calender API return object source:
# https://developers.google.com/workspace/calendar/api/v3/reference/events

# Tasks API return object source:
# https://developers.google.com/tasks/reference/rest/v1/tasks

def main():
	calendar_cfg = load_calendar_config()
	tasks_cfg = load_tasks_config()

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
	# 	calendar_service, cfg, calendar_key="academic",
	# 	course_code="COMP1934", class_type="Lecture 2",
	# 	day_of_week=2, start_time=datetime.time(8,0), end_time=datetime.time(11,0),
	# 	location="Building A, Room 101", description="epic lecture")

	# print("Current week study times (hours):", current_week(calendar_service, cfg))
	# print("Previous week study times (hours):", previous_week(calendar_service, cfg, weeks_ago=2))

	# discord_cfg = load_discord_config()
	# flush_sessions_to_calendar(calendar_service, discord_cfg, calendar_cfg)

	# tasklist_id = read_tasklist_id(tasks_service, "COMP2041")
	
	# create_week_tasks(tasks_service, tasklist_id, week_number=2,
	# 			   subtasks=["Lecture 1", "Tutorial"])
	
	create_weekly_tasks(tasks_service, "MATH2019", ["Lecture 1", "Tutorial"], 3, skip_breaks=True)



if __name__ == "__main__":
	main()