import datetime

from googleapiclient.errors import HttpError

def read_tasklists(service, maxResults=10):
	"""Return a list of task lists available to the user"""
	
	results = service.tasklists().list(maxResults=maxResults).execute()
	return results.get("items", [])

def read_upcoming_tasks(service, tasklist_id=None, max_results=10):
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