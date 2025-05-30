import customtkinter as ctk

from task import Task


class TodoListApp(ctk.CTk):
    """The main class of the To-Do List application with a CustomTkinter interface."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Do-Do List")
        self.geometry("400x500")
        self.resizable(False, False)

        self.tasks: list[Task] = []
        self.task_vars: list[ctk.BooleanVar] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Creates and displays interface elements (widgets)."""
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Enter a task...")
        self.task_entry.pack(padx=10, pady=(10, 5), fill="x")

        add_button = ctk.CTkButton(self, text="Add task", command=self.add_task)
        add_button.pack(padx=10, pady=5, fill="x")

        clear_button = ctk.CTkButton(
            self,
            text="Remove completed",
            command=self.delete_completed_task,
            fg_color="grey",
            hover_color="#555",
        )
        clear_button.pack(padx=10, pady=5, fill="x")

        self.task_frame = ctk.CTkScrollableFrame(self)
        self.task_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def add_task(self) -> None:
        """Adds a new task from the input field to the list and to the interface."""
        text = self.task_entry.get().strip()
        if not text:
            return

        task = Task(text)
        var = ctk.BooleanVar(value=task.completed)
        self.tasks.append(task)
        self.task_vars.append(var)

        self.task_entry.delete(0, "end")
        self._add_task_widget(task, var)

    def _add_task_widget(self, task: Task, var: ctk.BooleanVar) -> None:
        """Creates a visual task element (a row with a checkbox and a delete tool)."""
        index = len(self.tasks) - 1
        frame = ctk.CTkFrame(self.task_frame)
        frame.pack(fill="x", padx=2, pady=2)

        def toggle():
            task.completed = var.get()

        check = ctk.CTkCheckBox(
            frame,
            text=task.description,
            variable=var,
            command=toggle,
        )
        check.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(
            frame,
            text="❌",
            width=30,
            fg_color="#b03737",
            hover_color="#a00",
            command=lambda: self.delete_task(index),
        )
        delete_btn.pack(side="right", padx=2)
        task.widget_frame = frame

    def delete_task(self, index: int) -> None:
        """Deletes a task and its widget by index."""
        if 0 <= index < len(self.tasks):
            frame = self.tasks[index].widget_frame
            if frame is not None:
                frame.destroy()
            del self.tasks[index]
            del self.task_vars[index]
            self._refresh_ui()

    def _refresh_ui(self) -> None:
        """Updates the delete task button commands so that they respond correctly to new indexes."""

        for i, task in enumerate(self.tasks):
            if task.widget_frame is not None:
                for widget in task.widget_frame.winfo_children():
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(command=lambda i=i: self.delete_task(i))

    def delete_completed_task(self) -> None:
        """Deletes all tasks that are marked as completed."""

        for i in reversed(range(len(self.tasks))):
            if self.tasks[i].completed:
                frame = self.tasks[i].widget_frame
                if frame is not None:
                    frame.destroy()
                del self.tasks[i]
                del self.task_vars[i]
        self._refresh_ui()