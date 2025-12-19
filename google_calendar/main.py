from .auth import get_credentials
from .service import get_calendar_service, get_tasks_service

from .calendar.queries import read_upcoming_events
from .calendar.utils import print_events

from .tasks.queries import read_upcoming_tasks
from .tasks.utils import print_tasks


# Calender API return object source:
# https://developers.google.com/workspace/calendar/api/v3/reference/events

# Tasks API return object source:
# https://developers.google.com/tasks/reference/rest/v1/tasks

def main():	
	creds = get_credentials()
	calendar_service = get_calendar_service(creds)
	tasks_service = get_tasks_service(creds)

	# print("Upcoming Calendar Events")
	# events = read_upcoming_events(calendar_service)
	# print_events(events)

	print("Upcoming Tasks")
	tasks = read_upcoming_tasks(tasks_service)
	print_tasks(tasks, fields=["title", "due", "notes"])
	

if __name__ == "__main__":
	main()