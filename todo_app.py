
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store users and tasks
USER_FILE = "users.json"
TASK_FILE = "tasks.json"

# Initialize files if they don't exist
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"demo@redx.com": "demo123"}, f)

if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w") as f:
        json.dump({}, f)

# Load users and tasks
with open(USER_FILE, "r") as f:
    users = json.load(f)

with open(TASK_FILE, "r") as f:
    tasks = json.load(f)

current_user = None

# Login/Register window
def login_window():
    global current_user
    win = tk.Tk()
    win.title("Login")
    win.geometry("300x200")

    tk.Label(win, text="Email").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Password").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def login():
        email = email_entry.get()
        pw = pass_entry.get()
        if email in users and users[email] == pw:
            global current_user
            current_user = email
            win.destroy()
            todo_window()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register():
        email = email_entry.get()
        pw = pass_entry.get()
        if email in users:
            messagebox.showerror("Error", "User already exists")
        else:
            users[email] = pw
            with open(USER_FILE, "w") as f:
                json.dump(users, f)
            messagebox.showinfo("Success", "Registered! Now login.")

    tk.Button(win, text="Login", command=login).pack(pady=5)
    tk.Button(win, text="Register", command=register).pack()
    win.mainloop()


# Main To-Do window
def todo_window():
    win = tk.Tk()
    win.title(f"{current_user}'s To-Do List")
    win.geometry("400x400")

    # Load user tasks
    user_tasks = tasks.get(current_user, [])

    listbox = tk.Listbox(win, width=50, height=15)
    listbox.pack(pady=10)
    for t in user_tasks:
        status = "✅" if t["completed"] else "❌"
        listbox.insert(tk.END, f"{status} {t['title']}")

    def refresh():
        listbox.delete(0, tk.END)
        user_tasks = tasks.get(current_user, [])
        for t in user_tasks:
            status = "✅" if t["completed"] else "❌"
            listbox.insert(tk.END, f"{status} {t['title']}")

    def add_task():
        title = simpledialog.askstring("New Task", "Task title:")
        if title:
            user_tasks.append({"title": title, "completed": False})
            tasks[current_user] = user_tasks
            with open(TASK_FILE, "w") as f:
                json.dump(tasks, f)
            refresh()

    def edit_task():
        selected = listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        title = simpledialog.askstring("Edit Task", "New title:", initialvalue=user_tasks[idx]["title"])
        if title:
            user_tasks[idx]["title"] = title
            tasks[current_user] = user_tasks
            with open(TASK_FILE, "w") as f:
                json.dump(tasks, f)
            refresh()

    def delete_task():
        selected = listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        del user_tasks[idx]
        tasks[current_user] = user_tasks
        with open(TASK_FILE, "w") as f:
            json.dump(tasks, f)
        refresh()

    def toggle_task():
        selected = listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        user_tasks[idx]["completed"] = not user_tasks[idx]["completed"]
        tasks[current_user] = user_tasks
        with open(TASK_FILE, "w") as f:
            json.dump(tasks, f)
        refresh()

    tk.Button(win, text="Add Task", command=add_task).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(win, text="Edit Task", command=edit_task).pack(side=tk.LEFT, padx=5)
    tk.Button(win, text="Delete Task", command=delete_task).pack(side=tk.LEFT, padx=5)
    tk.Button(win, text="Toggle Complete", command=toggle_task).pack(side=tk.LEFT, padx=5)

    win.mainloop()


# Run the app
login_window()
