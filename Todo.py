import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Style To-Do App")
        self.root.configure(bg="black")
        self.root.geometry("800x600")

        self.todo_lists = {}

        self.cards_frame = tk.Frame(root, bg="black")
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.plus_button = tk.Button(
            root, text="+", font=("Arial", 24, "bold"), bg="gold", fg="black",
            bd=0, command=self.add_new_list
        )
        self.plus_button.place(relx=0.9, rely=0.85, anchor="center", width=60, height=60)

        self.render_cards()

    def render_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for list_name, list_data in self.todo_lists.items():
            frame = tk.Frame(self.cards_frame, bg="#1e1e1e")
            frame.pack(fill="x", pady=10, padx=10)

            title = tk.Label(frame, text=list_name, fg="white", bg="#1e1e1e",
                             font=("Arial", 14, "bold"), anchor="w")
            title.pack(fill="x")

            preview_text = "\n".join(task for task in list_data["tasks"][:3])
            if len(list_data["tasks"]) > 3:
                preview_text += "\n..."
            preview = tk.Label(frame, text=preview_text, fg="lightgray", bg="#1e1e1e",
                               font=("Arial", 12), anchor="w", justify="left")
            preview.pack(fill="x")

            updated_label = tk.Label(frame, text=list_data["last_updated"], fg="gray", bg="#1e1e1e",
                                     font=("Arial", 10), anchor="w")
            updated_label.pack(fill="x", pady=(5, 0))

            frame.bind("<Button-1>", lambda e, name=list_name: self.open_task_window(name))
            title.bind("<Button-1>", lambda e, name=list_name: self.open_task_window(name))
            preview.bind("<Button-1>", lambda e, name=list_name: self.open_task_window(name))

    def add_new_list(self):
        list_name = simpledialog.askstring("New List", "Enter list name:")
        if list_name and list_name not in self.todo_lists:
            self.todo_lists[list_name] = {
                "tasks": [],
                "completed": [],
                "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            self.render_cards()

    def open_task_window(self, list_name):
        win = tk.Toplevel(self.root)
        win.title(list_name)
        win.configure(bg="black")
        win.geometry("400x500")

        tasks_frame = tk.Frame(win, bg="black")
        tasks_frame.pack(fill="both", expand=True, pady=10)

        def update_list_ui():
            for widget in tasks_frame.winfo_children():
                widget.destroy()
            for idx, task in enumerate(self.todo_lists[list_name]["tasks"]):
                var = tk.BooleanVar(value=(task in self.todo_lists[list_name]["completed"]))
                cb = tk.Checkbutton(tasks_frame, text=task, variable=var,
                                    onvalue=True, offvalue=False,
                                    command=lambda t=task, v=var: self.toggle_task(list_name, t, v),
                                    fg="white", bg="black", selectcolor="black", font=("Arial", 12), anchor="w")
                cb.pack(fill="x", padx=20, pady=5)
                btn_frame = tk.Frame(tasks_frame, bg="black")
                btn_frame.pack(fill="x", padx=20)
                tk.Button(btn_frame, text="Edit", command=lambda t=task: self.edit_task(list_name, t, update_list_ui)).pack(side="left")
                tk.Button(btn_frame, text="Delete", command=lambda t=task: self.delete_task(list_name, t, update_list_ui)).pack(side="right")

        def add_task():
            task = simpledialog.askstring("Add Task", "Enter new task:")
            if task:
                self.todo_lists[list_name]["tasks"].append(task)
                self.todo_lists[list_name]["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                update_list_ui()
                self.render_cards()

        update_list_ui()

        tk.Button(win, text="Add Task", command=add_task, bg="gold", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

    def toggle_task(self, list_name, task, var):
        if var.get():
            if task not in self.todo_lists[list_name]["completed"]:
                self.todo_lists[list_name]["completed"].append(task)
        else:
            if task in self.todo_lists[list_name]["completed"]:
                self.todo_lists[list_name]["completed"].remove(task)
        self.todo_lists[list_name]["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.render_cards()

    def delete_task(self, list_name, task, refresh_ui):
        self.todo_lists[list_name]["tasks"].remove(task)
        if task in self.todo_lists[list_name]["completed"]:
            self.todo_lists[list_name]["completed"].remove(task)
        self.todo_lists[list_name]["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        refresh_ui()
        self.render_cards()

    def edit_task(self, list_name, task, refresh_ui):
        new_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=task)
        if new_task:
            idx = self.todo_lists[list_name]["tasks"].index(task)
            self.todo_lists[list_name]["tasks"][idx] = new_task
            if task in self.todo_lists[list_name]["completed"]:
                self.todo_lists[list_name]["completed"].remove(task)
                self.todo_lists[list_name]["completed"].append(new_task)
            self.todo_lists[list_name]["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            refresh_ui()
            self.render_cards()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
