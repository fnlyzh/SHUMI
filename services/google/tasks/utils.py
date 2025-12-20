
def print_tasks(tasks, fields=None) -> None:
    """ 
    Prints a subset of fields of a list of tasks.

    Args:
        tasks: list of Task objects from Google Tasks API
        fields: subset of fields; leave empty to print all fields
    """
    for task in tasks:
        print_task(task, fields)

def print_task(task, fields=None) -> None:
    """
    Prints a subset of fields of a task.

    Args:
        task: Task object from Google Tasks API
        fields: subset of fields; leave empty to print all fields
    """

    if fields is None:
        print(task)
    else:
        for field in fields:
            print(f"{field.capitalize()}: {task.get(field, "(empty)")}")
