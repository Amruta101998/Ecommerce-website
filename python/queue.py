import heapq

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.task_id_counter = 1

    def add_task(self, priority, description):
        task = (priority, self.task_id_counter, description)
        heapq.heappush(self.tasks, task)
        self.task_id_counter += 1

    def get_next_task(self):
        if self.tasks:
            return heapq.heappop(self.tasks)
        else:
            return None

    def display_tasks(self):
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
