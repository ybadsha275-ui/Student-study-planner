import customtkinter as ctk
from datetime import date, datetime

from core.task_manager import (
    load_tasks,
    get_task_progress,
    load_study_data,
    save_study_data
)


class PlannerView(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_header()
        self.create_goal_section()
        self.create_summary()
        self.create_plan()

        self.generate_plan()

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def create_header(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text="Smart Daily Planner",
            font=("Segoe UI", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            frame,
            text="Let the planner decide what deserves your attention first.",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            frame,
            text="Generate New Plan",
            width=160,
            command=self.generate_plan
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10
        )

    # ---------------------------------------------------------
    # GOAL
    # ---------------------------------------------------------

    def create_goal_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        data = load_study_data()

        ctk.CTkLabel(
            card,
            text="Daily Study Goal",
            font=("Segoe UI", 14, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15
        )

        self.goal_var = ctk.StringVar(
            value=str(
                data.get("daily_goal", 5)
            )
        )

        ctk.CTkEntry(
            card,
            textvariable=self.goal_var,
            width=100
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=15,
            sticky="w"
        )

        ctk.CTkLabel(
            card,
            text="tasks",
            font=("Segoe UI", 12)
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ctk.CTkButton(
            card,
            text="Save Goal",
            width=110,
            command=self.save_goal
        ).grid(
            row=0,
            column=3,
            padx=15
        )

    def save_goal(self):

        try:
            goal = max(
                1,
                int(self.goal_var.get())
            )
        except ValueError:
            goal = 5

        data = load_study_data()
        data["daily_goal"] = goal
        save_study_data(data)

        self.goal_var.set(str(goal))

        self.generate_plan()

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def create_summary(self):

        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        for column in range(3):
            self.summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

    def create_summary_card(
        self,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
            corner_radius=14
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 11),
            text_color=("gray40", "gray65")
        ).pack(
            pady=(12, 3)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(0, 12)
        )

    # ---------------------------------------------------------
    # PLAN
    # ---------------------------------------------------------

    def create_plan(self):

        self.plan_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=15
        )

        self.plan_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(5, 20)
        )

    def generate_plan(self):

        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        for widget in self.plan_frame.winfo_children():
            widget.destroy()

        data = load_study_data()

        try:
            goal = max(
                1,
                int(self.goal_var.get())
            )
        except ValueError:
            goal = 5

        self.goal_var.set(str(goal))

        tasks = [
            task
            for task in load_tasks()
            if not task.get("completed")
        ]

        today = date.today()

        def ranking(task):

            priority_score = {
                "High": 3,
                "Medium": 2,
                "Low": 1
            }.get(
                task.get("priority"),
                1
            )

            difficulty_score = {
                "Hard": 3,
                "Medium": 2,
                "Easy": 1
            }.get(
                task.get("difficulty"),
                1
            )

            due_score = 0

            due = task.get("due_date", "")

            if due:

                try:
                    due_date = datetime.strptime(
                        due,
                        "%Y-%m-%d"
                    ).date()

                    difference = (
                        due_date - today
                    ).days

                    if difference < 0:
                        due_score = 100
                    elif difference == 0:
                        due_score = 80
                    elif difference <= 2:
                        due_score = 50
                    elif difference <= 7:
                        due_score = 20

                except ValueError:
                    pass

            progress_score = (
                100 - get_task_progress(task)
            ) / 100

            return (
                due_score
                + priority_score * 15
                + difficulty_score * 5
                + progress_score * 10
            )

        tasks.sort(
            key=ranking,
            reverse=True
        )

        planned = tasks[:goal]

        total_minutes = sum(
            task.get("estimated_minutes", 30)
            for task in planned
        )

        self.create_summary_card(
            0,
            "Today's Plan",
            f"{len(planned)} tasks"
        )

        self.create_summary_card(
            1,
            "Estimated Time",
            f"{total_minutes} min"
        )

        self.create_summary_card(
            2,
            "Focus Blocks",
            str(max(1, round(total_minutes / 25)))
        )

        if not planned:

            ctk.CTkLabel(
                self.plan_frame,
                text="🎉 Nothing urgent!\n\nYour pending task list is empty.",
                font=("Segoe UI", 20, "bold")
            ).pack(
                pady=100
            )

            return

        ctk.CTkLabel(
            self.plan_frame,
            text="Recommended Study Order",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 12)
        )

        for index, task in enumerate(planned, start=1):

            self.create_plan_card(
                index,
                task
            )

    def create_plan_card(
        self,
        index,
        task
    ):

        card = ctk.CTkFrame(
            self.plan_frame,
            corner_radius=14
        )

        card.pack(
            fill="x",
            padx=8,
            pady=6
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text=str(index),
            font=("Segoe UI", 18, "bold"),
            width=40
        ).grid(
            row=0,
            column=0,
            rowspan=3,
            padx=15
        )

        ctk.CTkLabel(
            card,
            text=task.get("task", ""),
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=(12, 2)
        )

        detail = (
            f"{task.get('subject') or 'General'} • "
            f"{task.get('priority', 'Medium')} priority • "
            f"{task.get('estimated_minutes', 30)} min"
        )

        ctk.CTkLabel(
            card,
            text=detail,
            font=("Segoe UI", 11),
            text_color=("gray40", "gray65"),
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="w"
        )

        reason = self.get_reason(task)

        ctk.CTkLabel(
            card,
            text=reason,
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(3, 12)
        )

        ctk.CTkButton(
            card,
            text="Open Tasks",
            width=100,
            command=self.app.show_tasks
        ).grid(
            row=0,
            column=2,
            rowspan=3,
            padx=15
        )

    def get_reason(self, task):

        if task.get("due_date") == date.today().isoformat():
            return "🔥 Priority recommendation: due today"

        if task.get("priority") == "High":
            return "⚡ Priority recommendation: high-priority task"

        if task.get("difficulty") == "Hard":
            return "🧠 Good choice for a focused study block"

        if task.get("starred"):
            return "⭐ Marked important"

        return "📚 Recommended based on your current workload"