import customtkinter as ctk
from tkinter import messagebox

from core.task_manager import (
    load_tasks,
    add_task,
    update_task,
    toggle_completion,
    toggle_subtask,
    toggle_star,
    delete_task,
    get_due_status,
    get_task_progress,
    filter_tasks,
    sort_tasks
)

from core.gamification import (
    load_gamification,
    award_task_xp,
    check_achievements,
    get_level,
    get_achievement_definitions
)


class TasksView(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.app = app

        self.search_var = ctk.StringVar(value="")
        self.priority_var = ctk.StringVar(value="All")
        self.status_var = ctk.StringVar(value="All")
        self.category_var = ctk.StringVar(value="All")
        self.difficulty_var = ctk.StringVar(value="All")
        self.sort_var = ctk.StringVar(value="Default")
        self.starred_var = ctk.BooleanVar(value=False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_filters()
        self.create_task_list()

        self.refresh()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="My Tasks",
            font=("Segoe UI", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Manage tasks, subtasks, deadlines and earn XP.",
            font=("Segoe UI", 13),
            text_color=("gray35", "gray65")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0)
        )

        ctk.CTkButton(
            header,
            text="+ Add Task",
            width=140,
            height=42,
            font=("Segoe UI", 14, "bold"),
            command=self.open_add_dialog
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(15, 0)
        )

    # =========================================================
    # FILTERS
    # =========================================================

    def create_filters(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 12)
        )

        for column in range(8):
            card.grid_columnconfigure(
                column,
                weight=1
            )

        ctk.CTkEntry(
            card,
            textvariable=self.search_var,
            placeholder_text="Search tasks..."
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=12,
            sticky="ew"
        )

        self.make_combo(
            card,
            self.priority_var,
            ["All", "High", "Medium", "Low"],
            1
        )

        self.make_combo(
            card,
            self.status_var,
            [
                "All",
                "Completed",
                "Due Today",
                "Upcoming",
                "Overdue",
                "No Due Date"
            ],
            2
        )

        self.make_combo(
            card,
            self.category_var,
            [
                "All",
                "Study",
                "Assignment",
                "Exam",
                "Project",
                "Revision",
                "Other"
            ],
            3
        )

        self.make_combo(
            card,
            self.difficulty_var,
            [
                "All",
                "Easy",
                "Medium",
                "Hard"
            ],
            4
        )

        self.make_combo(
            card,
            self.sort_var,
            [
                "Default",
                "Priority",
                "Due Date",
                "Study Time",
                "Difficulty",
                "Progress",
                "Name"
            ],
            5
        )

        ctk.CTkCheckBox(
            card,
            text="Starred",
            variable=self.starred_var,
            command=self.refresh
        ).grid(
            row=0,
            column=6,
            padx=8
        )

        ctk.CTkButton(
            card,
            text="Clear",
            width=80,
            command=self.clear_filters
        ).grid(
            row=0,
            column=7,
            padx=8
        )

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

        self.priority_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

        self.status_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

        self.category_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

        self.difficulty_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

        self.sort_var.trace_add(
            "write",
            lambda *_: self.refresh()
        )

    def make_combo(
        self,
        parent,
        variable,
        values,
        column
    ):

        ctk.CTkComboBox(
            parent,
            variable=variable,
            values=values
        ).grid(
            row=0,
            column=column,
            padx=8,
            pady=12,
            sticky="ew"
        )

    # =========================================================
    # TASK LIST
    # =========================================================

    def create_task_list(self):

        self.task_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.task_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20)
        )

    def refresh(self):

        for widget in self.task_list.winfo_children():
            widget.destroy()

        tasks = load_tasks()

        query = self.search_var.get().strip().lower()

        if query:

            tasks = [
                task
                for task in tasks
                if query in task.get("task", "").lower()
                or query in task.get("subject", "").lower()
                or query in task.get("description", "").lower()
                or query in task.get("category", "").lower()
            ]

        tasks = filter_tasks(
            tasks,
            priority=self.priority_var.get(),
            status=self.status_var.get(),
            category=self.category_var.get(),
            difficulty=self.difficulty_var.get(),
            starred=self.starred_var.get()
        )

        tasks = sort_tasks(
            tasks,
            self.sort_var.get()
        )

        if not tasks:

            ctk.CTkLabel(
                self.task_list,
                text=(
                    "No tasks found.\n\n"
                    "Try changing the filters or add a new task."
                ),
                font=("Segoe UI", 17),
                text_color=("gray40", "gray65")
            ).pack(
                pady=100
            )

            return

        for task in tasks:
            self.create_task_card(task)

    # =========================================================
    # TASK CARD
    # =========================================================

    def create_task_card(self, task):

        card = ctk.CTkFrame(
            self.task_list,
            corner_radius=16
        )

        card.pack(
            fill="x",
            padx=5,
            pady=7
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        progress = get_task_progress(task)

        checkbox = ctk.CTkCheckBox(
            card,
            text="",
            width=25,
            command=lambda task_id=task["id"]:
            self.complete_task(task_id)
        )

        checkbox.grid(
            row=0,
            column=0,
            rowspan=5,
            padx=(15, 5),
            pady=15,
            sticky="n"
        )

        if task.get("completed"):
            checkbox.select()

        ctk.CTkLabel(
            card,
            text=task.get("task", "Untitled Task"),
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=10,
            pady=(15, 2)
        )

        info = (
            f"{task.get('subject') or 'No subject'}  •  "
            f"{task.get('category', 'Study')}  •  "
            f"{task.get('difficulty', 'Medium')}  •  "
            f"{task.get('estimated_minutes', 30)} min"
        )

        ctk.CTkLabel(
            card,
            text=info,
            font=("Segoe UI", 11),
            text_color=("gray40", "gray65"),
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=10
        )

        ctk.CTkLabel(
            card,
            text=self.get_due_text(task),
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=10,
            pady=(3, 5)
        )

        progress_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        progress_frame.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10
        )

        progress_frame.grid_columnconfigure(
            0,
            weight=1
        )

        bar = ctk.CTkProgressBar(
            progress_frame,
            height=8
        )

        bar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        bar.set(
            progress / 100
        )

        ctk.CTkLabel(
            progress_frame,
            text=f"{progress}%",
            font=("Segoe UI", 10),
            width=45
        ).grid(
            row=0,
            column=1,
            padx=(8, 0)
        )

        subtasks = task.get(
            "subtasks",
            []
        )

        if subtasks:

            done = sum(
                1
                for subtask in subtasks
                if subtask.get(
                    "completed",
                    False
                )
            )

            subtask_text = (
                f"Subtasks: {done}/{len(subtasks)}"
            )

        else:

            subtask_text = "No subtasks"

        ctk.CTkLabel(
            card,
            text=subtask_text,
            font=("Segoe UI", 10),
            anchor="w"
        ).grid(
            row=4,
            column=1,
            sticky="w",
            padx=10,
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.grid(
            row=0,
            column=2,
            rowspan=5,
            padx=10,
            pady=10
        )

        star_text = (
            "★"
            if task.get("starred", False)
            else "☆"
        )

        ctk.CTkButton(
            actions,
            text=star_text,
            width=36,
            command=lambda task_id=task["id"]:
            self.star_task(task_id)
        ).pack(
            pady=2
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            width=70,
            command=lambda task_id=task["id"]:
            self.open_edit_dialog(task_id)
        ).pack(
            pady=2
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=70,
            fg_color="#8B2E2E",
            hover_color="#A63D3D",
            command=lambda task_id=task["id"]:
            self.remove_task(task_id)
        ).pack(
            pady=2
        )

        # -----------------------------------------------------
        # SUBTASKS
        # -----------------------------------------------------

        if subtasks:

            subtask_frame = ctk.CTkFrame(
                self.task_list,
                corner_radius=12
            )

            subtask_frame.pack(
                fill="x",
                padx=25,
                pady=(0, 5)
            )

            ctk.CTkLabel(
                subtask_frame,
                text=f"Subtasks — {task.get('task', '')}",
                font=("Segoe UI", 12, "bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 4)
            )

            for subtask in subtasks:

                variable = ctk.BooleanVar(
                    value=subtask.get(
                        "completed",
                        False
                    )
                )

                ctk.CTkCheckBox(
                    subtask_frame,
                    text=subtask.get(
                        "text",
                        ""
                    ),
                    variable=variable,
                    command=lambda
                    task_id=task["id"],
                    subtask_id=subtask["id"]:
                    self.change_subtask(
                        task_id,
                        subtask_id
                    )
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=3
                )

    # =========================================================
    # COMPLETE TASK
    # =========================================================

    def complete_task(
        self,
        task_id
    ):

        old_task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None
        )

        if old_task is None:
            return

        was_completed = bool(
            old_task.get(
                "completed",
                False
            )
        )

        updated_task = toggle_completion(
            task_id
        )

        if (
            updated_task
            and not was_completed
            and updated_task.get(
                "completed",
                False
            )
        ):

            self.handle_task_xp(
                updated_task
            )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard"
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # SUBTASK
    # =========================================================

    def change_subtask(
        self,
        task_id,
        subtask_id
    ):

        old_task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None
        )

        was_completed = (
            bool(
                old_task.get(
                    "completed",
                    False
                )
            )
            if old_task
            else False
        )

        updated_task = toggle_subtask(
            task_id,
            subtask_id
        )

        if (
            updated_task
            and not was_completed
            and updated_task.get(
                "completed",
                False
            )
        ):

            self.handle_task_xp(
                updated_task
            )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard"
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # XP
    # =========================================================

    def handle_task_xp(
        self,
        task
    ):

        before = load_gamification()

        old_xp = int(
            before.get(
                "xp",
                0
            )
        )

        old_level = get_level(
            old_xp
        )

        earned = award_task_xp(
            task
        )

        if earned <= 0:
            return

        after = load_gamification()

        new_xp = int(
            after.get(
                "xp",
                0
            )
        )

        new_level = get_level(
            new_xp
        )

        new_achievements = check_achievements()

        if new_level > old_level:

            message = (
                f"You reached Level {new_level}!\n\n"
                f"+{earned} XP earned."
            )

            self.show_game_notification(
                "🎉 LEVEL UP!",
                message
            )

        elif new_achievements:

            names = self.get_achievement_names(
                new_achievements
            )

            message = (
                f"+{earned} XP earned!\n\n"
                + "\n".join(names)
            )

            self.show_game_notification(
                "🏆 Achievement Unlocked!",
                message
            )

        else:

            self.show_game_notification(
                "⭐ XP Earned",
                f"+{earned} XP"
            )

    # =========================================================
    # ACHIEVEMENT NAMES
    # =========================================================

    def get_achievement_names(
        self,
        achievement_ids
    ):

        definitions = {
            item["id"]: item
            for item in get_achievement_definitions()
        }

        names = []

        for achievement_id in achievement_ids:

            item = definitions.get(
                achievement_id
            )

            if item:

                names.append(
                    f"{item['icon']} {item['name']}"
                )

        return names

    # =========================================================
    # XP NOTIFICATION
    # =========================================================

    def show_game_notification(
        self,
        title,
        message
    ):

        notification = ctk.CTkToplevel(
            self
        )

        notification.title(
            title
        )

        notification.geometry(
            "380x210"
        )

        notification.resizable(
            False,
            False
        )

        notification.transient(
            self
        )

        card = ctk.CTkFrame(
            notification,
            corner_radius=15
        )

        card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 19, "bold")
        ).pack(
            pady=(20, 8)
        )

        ctk.CTkLabel(
            card,
            text=message,
            font=("Segoe UI", 12),
            justify="center",
            wraplength=320
        ).pack(
            padx=15
        )

        ctk.CTkButton(
            card,
            text="Nice!",
            width=100,
            command=notification.destroy
        ).pack(
            pady=15
        )

        notification.after(
            5000,
            lambda: (
                notification.destroy()
                if notification.winfo_exists()
                else None
            )
        )

    # =========================================================
    # STAR
    # =========================================================

    def star_task(
        self,
        task_id
    ):

        toggle_star(
            task_id
        )

        self.refresh()

    # =========================================================
    # DELETE
    # =========================================================

    def remove_task(
        self,
        task_id
    ):

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to permanently delete this task?"
        )

        if not confirm:
            return

        delete_task(
            task_id
        )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard"
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # FILTER RESET
    # =========================================================

    def clear_filters(self):

        self.search_var.set("")
        self.priority_var.set("All")
        self.status_var.set("All")
        self.category_var.set("All")
        self.difficulty_var.set("All")
        self.sort_var.set("Default")
        self.starred_var.set(False)

    # =========================================================
    # DUE DATE
    # =========================================================

    def get_due_text(
        self,
        task
    ):

        status = get_due_status(
            task
        )

        due_date = task.get(
            "due_date",
            ""
        )

        if not due_date:
            return "No due date"

        if status == "Completed":
            return f"✓ Completed • {due_date}"

        if status == "Overdue":
            return f"⚠ OVERDUE • {due_date}"

        if status == "Due Today":
            return f"● DUE TODAY • {due_date}"

        return f"Due • {due_date}"

    # =========================================================
    # ADD DIALOG
    # =========================================================

    def open_add_dialog(self):

        self.open_task_dialog()

    # =========================================================
    # EDIT DIALOG
    # =========================================================

    def open_edit_dialog(
        self,
        task_id
    ):

        task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None
        )

        if task:

            self.open_task_dialog(
                task
            )

    # =========================================================
    # TASK DIALOG
    # =========================================================

    def open_task_dialog(
        self,
        task=None
    ):

        is_edit = task is not None

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Edit Task"
            if is_edit
            else "Add Task"
        )

        dialog.geometry(
            "650x760"
        )

        dialog.minsize(
            600,
            650
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        container = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        container.grid_columnconfigure(
            1,
            weight=1
        )

        task_var = ctk.StringVar(
            value=(
                task.get("task", "")
                if is_edit
                else ""
            )
        )

        subject_var = ctk.StringVar(
            value=(
                task.get("subject", "")
                if is_edit
                else ""
            )
        )

        priority_var = ctk.StringVar(
            value=(
                task.get(
                    "priority",
                    "Medium"
                )
                if is_edit
                else "Medium"
            )
        )

        category_var = ctk.StringVar(
            value=(
                task.get(
                    "category",
                    "Study"
                )
                if is_edit
                else "Study"
            )
        )

        difficulty_var = ctk.StringVar(
            value=(
                task.get(
                    "difficulty",
                    "Medium"
                )
                if is_edit
                else "Medium"
            )
        )

        minutes_var = ctk.StringVar(
            value=(
                str(
                    task.get(
                        "estimated_minutes",
                        30
                    )
                )
                if is_edit
                else "30"
            )
        )

        due_var = ctk.StringVar(
            value=(
                task.get(
                    "due_date",
                    ""
                )
                if is_edit
                else ""
            )
        )

        recurring_var = ctk.StringVar(
            value=(
                task.get(
                    "recurring",
                    "None"
                )
                if is_edit
                else "None"
            )
        )

        def add_label(
            text,
            row
        ):

            ctk.CTkLabel(
                container,
                text=text,
                font=("Segoe UI", 12, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=8,
                pady=8
            )

        add_label(
            "Task Name",
            0
        )

        ctk.CTkEntry(
            container,
            textvariable=task_var,
            placeholder_text="e.g. Practice Java DSA"
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Subject",
            1
        )

        ctk.CTkEntry(
            container,
            textvariable=subject_var,
            placeholder_text="e.g. Java"
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Priority",
            2
        )

        ctk.CTkComboBox(
            container,
            variable=priority_var,
            values=[
                "High",
                "Medium",
                "Low"
            ]
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Category",
            3
        )

        ctk.CTkComboBox(
            container,
            variable=category_var,
            values=[
                "Study",
                "Assignment",
                "Exam",
                "Project",
                "Revision",
                "Other"
            ]
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Difficulty",
            4
        )

        ctk.CTkComboBox(
            container,
            variable=difficulty_var,
            values=[
                "Easy",
                "Medium",
                "Hard"
            ]
        ).grid(
            row=4,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Study Time (minutes)",
            5
        )

        ctk.CTkEntry(
            container,
            textvariable=minutes_var
        ).grid(
            row=5,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Due Date",
            6
        )

        ctk.CTkEntry(
            container,
            textvariable=due_var,
            placeholder_text="YYYY-MM-DD"
        ).grid(
            row=6,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        ctk.CTkLabel(
            container,
            text="Example: 2026-09-20",
            font=("Segoe UI", 10),
            text_color=("gray45", "gray65")
        ).grid(
            row=7,
            column=1,
            sticky="w",
            padx=8
        )

        add_label(
            "Recurring",
            8
        )

        ctk.CTkComboBox(
            container,
            variable=recurring_var,
            values=[
                "None",
                "Daily",
                "Weekly",
                "Monthly"
            ]
        ).grid(
            row=8,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        add_label(
            "Description",
            9
        )

        description_box = ctk.CTkTextbox(
            container,
            height=120
        )

        description_box.grid(
            row=9,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        if is_edit:

            description_box.insert(
                "1.0",
                task.get(
                    "description",
                    ""
                )
            )

        add_label(
            "Subtasks\n(one per line)",
            10
        )

        subtasks_box = ctk.CTkTextbox(
            container,
            height=170
        )

        subtasks_box.grid(
            row=10,
            column=1,
            sticky="ew",
            padx=8,
            pady=8
        )

        if is_edit:

            for subtask in task.get(
                "subtasks",
                []
            ):

                subtasks_box.insert(
                    "end",
                    subtask.get(
                        "text",
                        ""
                    )
                    + "\n"
                )

        def save():

            name = task_var.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Task",
                    "Please enter a task name."
                )

                return

            try:

                minutes = int(
                    minutes_var.get()
                )

                if minutes <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Invalid Study Time",
                    "Study time must be a positive number."
                )

                return

            due_date = due_var.get().strip()

            if due_date:

                try:

                    from datetime import datetime

                    datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    )

                except ValueError:

                    messagebox.showwarning(
                        "Invalid Date",
                        "Use YYYY-MM-DD format."
                    )

                    return

            description = description_box.get(
                "1.0",
                "end"
            ).strip()

            subtask_lines = [
                line.strip()
                for line in subtasks_box.get(
                    "1.0",
                    "end"
                ).splitlines()
                if line.strip()
            ]

            if is_edit:

                old_subtasks = {
                    item.get("text"): item
                    for item in task.get(
                        "subtasks",
                        []
                    )
                }

                processed = []

                for text in subtask_lines:

                    old = old_subtasks.get(
                        text
                    )

                    processed.append({
                        "id": (
                            old.get("id")
                            if old
                            else None
                        ),
                        "text": text,
                        "completed": (
                            old.get(
                                "completed",
                                False
                            )
                            if old
                            else False
                        )
                    })

                update_task(
                    task["id"],
                    task=name,
                    subject=subject_var.get().strip(),
                    priority=priority_var.get(),
                    category=category_var.get(),
                    difficulty=difficulty_var.get(),
                    estimated_minutes=minutes,
                    due_date=due_date,
                    recurring=recurring_var.get(),
                    description=description,
                    subtasks=processed
                )

            else:

                add_task(
                    task_name=name,
                    subject=subject_var.get().strip(),
                    priority=priority_var.get(),
                    category=category_var.get(),
                    difficulty=difficulty_var.get(),
                    estimated_minutes=minutes,
                    due_date=due_date,
                    recurring=recurring_var.get(),
                    description=description,
                    subtasks=subtask_lines
                )

            dialog.destroy()

            self.refresh()

            if hasattr(
                self.app,
                "refresh_dashboard"
            ):

                self.app.refresh_dashboard()

        buttons = ctk.CTkFrame(
            dialog
        )

        buttons.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=120,
            command=dialog.destroy
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text=(
                "Save Task"
                if is_edit
                else "Add Task"
            ),
            width=140,
            command=save
        ).pack(
            side="right",
            padx=5
        )

        dialog.bind(
            "<Escape>",
            lambda event: dialog.destroy()
        )

        dialog.bind(
            "<Control-Return>",
            lambda event: save()
        )

        dialog.focus_force()