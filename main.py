from pymongo import MongoClient
from task import TaskManager

def menu():
    print("\n======== TASK MANAGER ========")
    print("|| 1. Add New Task          ||"
          "\n|| 2. List All Tasks        ||"
          "\n|| 3. Filter Tasks          ||"
          "\n|| 4. Update Task           ||"
          "\n|| 5. Mark Task as Completed||"
          "\n|| 6. Delete Task           ||"
          "\n|| 7. Exit                  ||"
          "\n==============================")
#time.sleep(2)
def main():
    # MongoDB Connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client["task_manager"]
    task_records = db["tasks"]

    manager = TaskManager(task_records)

    while True:
        menu()
        choice = input("Pick an option: ").strip()

        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            manager.filter_tasks()
        elif choice == "4":
            manager.update_task()
        elif choice == "5":
            manager.mark_completed()
        elif choice == "6":
            manager.delete_task()
        elif choice == "7":
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
