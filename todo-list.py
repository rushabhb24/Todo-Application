import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Task:
    def __init__(self, description, priority="Medium", due_date=None, completed=False):
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data["description"],
            priority=data.get("priority", "Medium"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
        )

    def __str__(self):
        status = "✔️ Completed" if self.completed else "❌ Pending"
        due_info = f" | Due: {self.due_date}" if self.due_date else ""
        return f"[{self.priority}] {self.description} - {status}{due_info}"


class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List Application")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f4ff")  # Light background

        self.filename = "tasks.json"
        self.tasks = []
        self.load_tasks()

        # --- Title ---
        tk.Label(
            root,
            text="🌟 My To-Do List 🌟",
            font=("Helvetica", 18, "bold"),
            bg="#6c63ff",
            fg="white",
            pady=10
        ).pack(fill="x")

        # --- Task Description ---
        tk.Label(root, text="Task Description:", font=("Arial", 11, "bold"), bg="#f0f4ff").pack(pady=(10, 0))
        self.task_entry = tk.Entry(root, width=50, font=("Arial", 11))
        self.task_entry.pack(pady=5)

        # --- Priority ---
        tk.Label(root, text="Priority:", font=("Arial", 11, "bold"), bg="#f0f4ff").pack()
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(root, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.config(font=("Arial", 10), bg="#dcd6ff")
        self.priority_menu.pack(pady=5)

        # --- Due Date ---
        tk.Label(root, text="Due Date (YYYY-MM-DD):", font=("Arial", 11, "bold"), bg="#f0f4ff").pack()
        self.due_entry = tk.Entry(root, width=30, font=("Arial", 11))
        self.due_entry.insert(0, "YYYY-MM-DD (optional)")
        self.due_entry.pack(pady=5)

        # --- Buttons Frame ---
        button_frame = tk.Frame(root, bg="#f0f4ff")
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="➕ Add Task", font=("Arial", 11, "bold"),
                                    bg="#4CAF50", fg="white", width=15, command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.complete_button = tk.Button(button_frame, text="✔️ Mark Completed", font=("Arial", 11, "bold"),
                                         bg="#2196F3", fg="white", width=15, command=self.complete_task)
        self.complete_button.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(button_frame, text="🔍 Search Task", font=("Arial", 11, "bold"),
                                       bg="#FF9800", fg="white", width=15, command=self.search_task)
        self.search_button.grid(row=0, column=2, padx=5)

        self.delete_button = tk.Button(button_frame, text="🗑️ Delete Task", font=("Arial", 11, "bold"),
                                       bg="#f44336", fg="white", width=15, command=self.delete_task)
        self.delete_button.grid(row=0, column=3, padx=5)

        # --- Task List ---
        tk.Label(root, text="Your Tasks:", font=("Arial", 11, "bold"), bg="#f0f4ff").pack(pady=(10, 0))
        self.listbox = tk.Listbox(root, width=90, height=12, font=("Consolas", 11),
                                  bg="#fff", fg="#333", selectbackground="#a29bfe")
        self.listbox.pack(pady=10)

        # --- Footer ---
        footer = tk.Label(
            root,
            text="❤️ Made with love by Tushar Bansod ❤️",
            font=("Arial", 10, "italic"),
            bg="#6c63ff",
            fg="white",
            pady=5
        )
        footer.pack(side="bottom", fill="x")

        self.refresh_list()

    # --- Data Handling ---
    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
        except FileNotFoundError:
            self.tasks = []

    def refresh_list(self, tasks=None):
        self.listbox.delete(0, tk.END)
        if tasks is None:
            tasks = self.tasks
        for task in tasks:
            self.listbox.insert(tk.END, str(task))

    # --- Task Functions ---
    def add_task(self):
        desc = self.task_entry.get().strip()
        if not desc:
            messagebox.showwarning("⚠️ Warning", "Task description cannot be empty!")
            return
        priority = self.priority_var.get()
        due_date = self.due_entry.get().strip()
        if due_date == "YYYY-MM-DD (optional)" or due_date == "":
            due_date = None
        task = Task(desc, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_list()
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, "YYYY-MM-DD (optional)")

    def complete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index].mark_completed()
            self.save_tasks()
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("⚠️ Warning", "Please select a task to complete!")

    def search_task(self):
        keyword = simpledialog.askstring("Search", "Enter keyword:")
        if keyword:
            results = [t for t in self.tasks if keyword.lower() in t.description.lower()]
            if results:
                self.refresh_list(results)
            else:
                messagebox.showinfo("🔍 Result", "No matching tasks found.")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this task?")
            if confirm:
                del self.tasks[index]
                self.save_tasks()
                self.refresh_list()
        except IndexError:
            messagebox.showwarning("⚠️ Warning", "Please select a task to delete!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
