import heapq

class TaskManager:
    """Manages a priority queue of tasks.

    This class provides functionality to add tasks with priorities,
    retrieve the highest priority task, and display all current tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task queue.

        Attributes:
            tasks (list): A heap-based priority queue storing tasks.
            task_id_counter (int): Counter for generating unique task IDs.
        """
        self.tasks = []
        self.task_id_counter = 1
 
    def add_task(self, priority, description):
        """Add a new task to the priority queue.

        Args:
            priority (int): The priority level of the task (lower values = higher priority).
            description (str): A description of the task.
        """
        task = (priority, self.task_id_counter, description)
        heapq.heappush(self.tasks, task)
        self.task_id_counter += 1
 
    def get_next_task(self):
        """Retrieve and remove the highest priority task from the queue.
 
        Returns:
            tuple: A tuple of (priority, task_id, description) for the next task,
                   or None if the queue is empty.
        """
        if self.tasks:
            return heapq.heappop(self.tasks)
        else:
            return None
 
    def display_tasks(self):
        """Display all current tasks in the queue.

        Prints each task with its ID, priority level, and description.
        """
        print("Current Tasks:")
        for task in self.tasks:
            print(f"Task ID: {task[1]}, Priority: {task[0]}, Description: {task[2]}")

# Example Usage
if __name__ == "__main__":
    task_manager = TaskManager()

    task_manager.add_task(2, "Implement feature A")
    task_manager.add_task(1, "Fix bug in module B")
    task_manager.add_task(3, "Write documentation")

    task_manager.display_tasks()

    next_task = task_manager.get_next_task()
    if next_task:
        print(f"Next Task: Priority {next_task[0]}, Description: {next_task[2]}")
    else:
        print("No tasks available.")
