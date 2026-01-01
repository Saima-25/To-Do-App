import sys
from src.services.task_service import TaskService


def display_menu():
    print("\n--- TODO APPLICATION ---")
    print("\n1. Add task")
    print("2. View all tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Mark task complete")
    print("6. Mark task incomplete")
    print("7. Exit")
    print("\nEnter your choice (1-7): ", end="")


def add_task(service):
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    try:
        task = service.add(title, description)
        print(f"Success: Task {task.id} added.")
    except ValueError as e:
        print(f"Error: {e}")


def view_tasks(service):
    tasks = service.list_all()
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- Task List ---")
    for task in tasks:
        status_symbol = "[X]" if task.status.value == "complete" else "[ ]"
        print(f"ID: {task.id} | {status_symbol} {task.title}")
        if task.description:
            print(f"   Description: {task.description}")


def update_task(service):
    try:
        task_id_input = input("Enter task ID: ")
        if not task_id_input:
            print("Error: ID is required.")
            return
        task_id = int(task_id_input)

        task = service.get(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        new_title = input(f"Enter new title (leave blank to keep old): ")
        new_description = input(f"Enter new description (leave blank to keep old): ")

        service.update(
            task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None
        )
        print(f"Success: Task {task_id} updated.")
    except ValueError:
        print("Error: Invalid input. ID must be a number.")


def delete_task(service):
    try:
        task_id_input = input("Enter task ID: ")
        if not task_id_input:
            print("Error: ID is required.")
            return
        task_id = int(task_id_input)
        service.delete(task_id)
        print(f"Success: Task {task_id} deleted.")
    except ValueError as e:
        if "Invalid input" in str(e): # Handle non-integer
             print("Error: Invalid input. ID must be a number.")
        else:
             print(f"Error: {e}")


def mark_complete(service):
    try:
        task_id_input = input("Enter task ID: ")
        if not task_id_input:
            print("Error: ID is required.")
            return
        task_id = int(task_id_input)
        service.mark_complete(task_id)
        print(f"Success: Task {task_id} marked complete.")
    except ValueError as e:
        print(f"Error: {e}")


def mark_incomplete(service):
    try:
        task_id_input = input("Enter task ID: ")
        if not task_id_input:
            print("Error: ID is required.")
            return
        task_id = int(task_id_input)
        service.mark_incomplete(task_id)
        print(f"Success: Task {task_id} marked incomplete.")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    service = TaskService()

    while True:
        display_menu()
        choice = input().strip()

        if choice == '1':
            add_task(service)
        elif choice == '2':
            view_tasks(service)
        elif choice == '3':
            update_task(service)
        elif choice == '4':
            delete_task(service)
        elif choice == '5':
            mark_complete(service)
        elif choice == '6':
            mark_incomplete(service)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
