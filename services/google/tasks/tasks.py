import datetime
import time

from googleapiclient.errors import HttpError

from config.handler import load_tasks_config, save_tasks_config, load_calendar_config

def read_tasklists(service, maxResults=20):
	"""Return a list of task lists available to the user"""
	
	results = service.tasklists().list(maxResults=maxResults).execute()
	return results.get("items", [])

def read_upcoming_tasks(service, tasklist_id=None, max_results=20):
	"""
	Reads some tasks from a given task list.
	
	Args:
		service: Google Tasks service
		tasklist_id: ID of task list to read tasks from
		max_results: max number of tasks to return
	
	Returns:
		list: tasks
	"""

	now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

	try:
		if tasklist_id is None:
			tasklist_id = read_default_tasklist_id(service)
			if tasklist_id is None:
				return []

		now = datetime.datetime.now(datetime.timezone.utc)
		week_end = now + datetime.timedelta(days=7)

		due_min = now.isoformat()
		due_max = week_end.isoformat()

		tasks_result = service.tasks().list(
			tasklist=tasklist_id,
			showCompleted=False,
			dueMin=due_min,
			dueMax=due_max,
			maxResults=max_results
		).execute()

		return tasks_result.get("items", [])
	
	except HttpError as error:
		print(f"Google API Error: {error}")
		return []

def read_default_tasklist_id(service):
	""" Reads the tasklist ID of the default tasklist. """
	tasklists = read_tasklists(service)
	if not tasklists:
		return None
	return tasklists[0]["id"]

def read_tasklist_id(service, name):
	""" Reads the tasklist ID of the tasklist with given name """
	tasks_cfg = load_tasks_config()


	tasklist_id = tasks_cfg.tasklists.get(name, 0)
	if tasklist_id != 0:
		return tasklist_id


	try:
		api_tasklists = read_tasklists(service)	
		for tl in api_tasklists:
			if tl["title"] == name:
				save_tasks_config(name, tl["id"])
				return tl["id"]

	except HttpError as e:
		raise RuntimeError(f"Google Tasks API error: {e}")


def create_week_tasks(service, tasklist_id: str, week_number: int, subtasks: list[str]):
	try:
		parent = service.tasks().insert(tasklist=tasklist_id, body={"title": f"Week {week_number}"}).execute()

		parent_id = parent["id"]

		for title in subtasks:
			service.tasks().insert(
				tasklist=tasklist_id,
				parent=parent_id,
				body={
					"title": title,
					"notes": f"Week {week_number}"
				}
			).execute()

	except HttpError as e:
		print(f"Google Tasks API error: {e}")

def create_weekly_tasks(service, tasklist_name, tasks, weeks, skip_breaks=True):
	calendar_cfg = load_calendar_config()
	if weeks is None:
		weeks = calendar_cfg.term_weeks

	tasklist_id = read_tasklist_id(service, tasklist_name)

	tasks_cfg = load_tasks_config()
	batch_size = tasks_cfg.rate_limit["batch_size"]
	sleep_seconds = tasks_cfg.rate_limit["sleep_seconds"]

	batch_counter = 0
	for week in range(1, weeks + 1):
		if skip_breaks and week in calendar_cfg.break_weeks:
			continue

		try:
			create_week_tasks(
				service,
				tasklist_id=tasklist_id,
				week_number=week,
				subtasks=tasks,
			)

			batch_counter += 1
			if batch_counter >= batch_size:
				time.sleep(sleep_seconds)
				batch_counter = 0

		except HttpError as e:
			print(f"Google Tasks API error (week {week}): {e}")