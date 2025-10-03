# todo.py

# -----------------------------
# Load and Save Tasks
# -----------------------------
def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

# -----------------------------
# View Tasks
# -----------------------------
def view_tasks(tasks):
    if not tasks:
        print("No tasks yet!")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

# -----------------------------
# Add Task
# -----------------------------
def add_task(tasks):
    task = input("Enter a new task: ")
    tasks.append(task)
    print(f"Task '{task}' added!")

# -----------------------------
# Complete Task
# -----------------------------
def complete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to complete: "))
        if 1 <= task_num <= len(tasks):
            completed = tasks.pop(task_num - 1)
            print(f"Task '{completed}' completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# -----------------------------
# Main Loop
# -----------------------------
def main():
    tasks = load_tasks()

    while True:
        print("\nOptions: view, add, complete, quit")
        choice = input("Choose an action: ").lower()

        if choice == "quit":
            save_tasks(tasks)
            print("Goodbye!")
            break
        elif choice == "view":
            view_tasks(tasks)
        elif choice == "add":
            add_task(tasks)
        elif choice == "complete":
            complete_task(tasks)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
