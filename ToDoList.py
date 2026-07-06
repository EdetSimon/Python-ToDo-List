import tkinter as tk
import json

tasks = []

def update_stats():
    total_tasks = len(tasks)
    completed_tasks = 0

    for checkbox, var in tasks:
        if var.get() == 1:
            completed_tasks += 1

    incomplete_tasks = total_tasks - completed_tasks
    total_label.config(text=f"Total Tasks: {total_tasks}")
    completed_label.config(text=f"Completed: {completed_tasks}")
    incomplete_label.config(text=f"Incomplete: {incomplete_tasks}")


def save_tasks():
    task_data = []

    for checkbox, var in tasks:
        task_data.append({
            "task": checkbox.cget("text"),
            "completed": var.get()
        })
    with open("tasks.json", "w") as file:
        json.dump(task_data, file)


def task_updated():
    update_stats()
    save_tasks()


def create_task(task_text, completed=0):

    task_var = tk.IntVar(value=completed)

    task_checkbox = tk.Checkbutton(task_frame, text=task_text, variable=task_var,command=task_updated, font=("Arial", 14))

    task_checkbox.pack(anchor="w")
    tasks.append((task_checkbox, task_var))



def add_task():
    task = task_entry.get().strip()

    if not task:
        return

    for checkbox, var in tasks:
        if checkbox.cget("text") == task:
            return

    create_task(task)

    save_tasks()
    update_stats()

    task_entry.delete(0,    tk.END)


def delete_task():
    for checkbox, var in tasks[:]:
        if var.get() == 1:
            checkbox.destroy()
            tasks.remove((checkbox, var))
    save_tasks()
    update_stats()

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            task_data = json.load(file)

        for item in task_data:

            create_task(item["task"], item["completed"])

        update_stats()
    except FileNotFoundError:
        pass


root = tk.Tk()
root.title("My To-Do List")
root.configure(bg="#F0F0F0")
root.geometry("450x650")
root.resizable(False, False)

main_frame = tk.Frame(root)
main_frame.pack(pady=20)
main_frame.configure(bg="#F0F0F0")

title_label = tk.Label(main_frame, text="My To-Do List", font=("Arial", 24, "bold"), bg="#F0F0F0")
title_label.pack(pady=20)

task_entry = tk.Entry(main_frame, width=30, font=("Arial", 14))
task_entry.pack(pady=10)

task_entry.bind("<Return>", lambda event: add_task())

add_button = tk.Button(main_frame, text="+ Add Task", command=add_task, width=20, font=("Arial", 14))
add_button.pack(pady=10)

delete_button = tk.Button(main_frame, text="Delete Selected", command=delete_task, font=("Arial", 14))
delete_button.pack(pady=5)

task_frame = tk.Frame(main_frame)
task_frame.pack(fill="both",pady=20)

total_label = tk.Label(main_frame, text="Total Tasks: 0", font=("Arial", 12), bg="#F0F0F0")
total_label.pack()
completed_label = tk.Label(main_frame, text="Completed: 0", font=("Arial", 12), bg="#F0F0F0")
completed_label.pack()
incomplete_label = tk.Label(main_frame, text="Incomplete: 0", font=("Arial", 12), bg="#F0F0F0")
incomplete_label.pack()


load_tasks()

root.mainloop()
