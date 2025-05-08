from datetime import datetime
from bson.objectid import ObjectId
import time


class Task:
    def __init__(self, title, description, due_date, priority): #__init__ is used to initialize the object
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = "Pending"
        self.created_at = datetime.now()

    def to_dict(self): #to_dict is used to convert the object to a dictionary because MongoDB stores data in dictionary format
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at
        }


#CRUD operations for the Task class
class TaskManager: #TaskManager is used to manage the tasks in the database
    def __init__(self, collection):
        self.collection = collection


#Create function to add a new task
    def add_task(self):
        print("\n>Add New Task")
        title = input("Title: ").strip()
        description = input("Description: ").strip()
        due_date = input("Due Date (YYYY-MM-DD): ").strip()
        priority = input("Priority (Low, Medium, High): ").strip().capitalize()

        task = Task(title, description, due_date, priority)
        self.collection.insert_one(task.to_dict())
        print("Task added successfully.")


#Read function to list all tasks or filter tasks
    def list_tasks(self):
        print("\n>All Tasks")
        for task in self.collection.find():
            self.print_task(task)

    def filter_tasks(self):
        print("\n>Filtered Tasks")
        field = input("Filter by (priority/status/due_date): ").strip()
        value = input("Value: ").strip()

        if field not in ["priority", "status", "due_date"]:
            print("Invalid filter.")
            return

        results = self.collection.find({field: value})
        for task in results:
            self.print_task(task)


#Update function to update an existing task
    def update_task(self):
        task_id = input(">Enter Task ID to update: ").strip()
        try:
            task = self.collection.find_one({"_id": ObjectId(task_id)})
        except:
            print("Invalid ID format.")
            return

        if not task:
            print("Task not found.")
            return

        print("Leave blank to keep current value.")
        title = input(f"Title [{task['title']}]: ") or task['title']
        description = input(f"Description [{task['description']}]: ") or task['description']
        due_date = input(f"Due Date [{task['due_date']}]: ") or task['due_date']
        priority = input(f"Priority [{task['priority']}]: ") or task['priority']

        update_data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority
        }

        self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
        print("Task updated successfully.")


#Function to mark a task as completed
    def mark_completed(self):
        task_id = input("Enter Task ID to mark as completed: ").strip()
        result = self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": "Completed"}}
        )
        if result.modified_count:
            print("Task marked as completed.")
        else:
            print("Task not found or already completed.")


#Delete function to delete a task
    def delete_task(self):
        task_id = input("Enter Task ID to delete: ").strip()
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count:
            print("Task deleted.")
        else:
            print("Task not found.")

    def print_task(self, task):
        print(f"\nID: {task['_id']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {task['status']}")
        print(f"Created At: {task['created_at']}")
        time.sleep(5) 
