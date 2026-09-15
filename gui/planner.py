import customtkinter as ctk

from datetime import date, datetime

from core.task_manager import (
    load_tasks,
    get_task_progress,
    load_study_data,
    save_study_data,
)


class PlannerView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        app,
    ):

        super().__init__(
            master,
            fg_color="transparent",
        )

        self.app = app

        # =====================================================
        # GLOBAL COLORS
        # =====================================================

        self.colors = getattr(
            app,
            "colors",
            {
                "accent": "#3B82F6",
                "accent_hover": "#2563EB",
                "card_dark": "#181F28",
                "card_light": "#FFFFFF",
                "border_dark": "#252E39",
                "border_light": "#E3E7ED",
                "text_dark": "#F3F4F6",
                "text_light": "#111827",
                "muted_dark": "#8B95A5",
                "muted_light": "#6B7280",
            },
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            3,
            weight=1,
        )

        self.create_header()
        self.create_goal_section()
        self.create_summary()
        self.create_plan()

        self.generate_plan()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 12),
        )

        frame.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        heading = ctk.CTkFrame(
            frame,
            fg_color="transparent",
        )

        heading.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            heading,
            text="INTELLIGENT STUDY PLANNING",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            heading,
            text="Smart Daily Planner",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            heading,
            text=(
                "Let the planner decide what deserves "
                "your attention first."
            ),
            font=("Segoe UI", 12),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

        # -----------------------------------------------------
        # GENERATE BUTTON
        # -----------------------------------------------------

        ctk.CTkButton(
            frame,
            text="✦  Generate New Plan",
            width=165,
            height=43,
            corner_radius=11,
            font=("Segoe UI", 11, "bold"),
            command=self.generate_plan,
        ).grid(
            row=0,
            column=1,
            padx=(15, 0),
        )

    # =========================================================
    # DAILY GOAL
    # =========================================================

    def create_goal_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # LEFT
        # -----------------------------------------------------

        info = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        info.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(18, 10),
            pady=15,
        )

        ctk.CTkLabel(
            info,
            text="🎯  DAILY TARGET",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            info,
            text="How many tasks should I plan?",
            font=("Segoe UI", 12, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # -----------------------------------------------------
        # GOAL INPUT
        # -----------------------------------------------------

        data = load_study_data()

        self.goal_var = ctk.StringVar(
            value=str(
                data.get(
                    "daily_goal",
                    5,
                )
            )
        )

        goal_entry = ctk.CTkEntry(
            card,
            textvariable=self.goal_var,
            width=75,
            height=38,
            corner_radius=9,
            justify="center",
        )

        goal_entry.grid(
            row=0,
            column=1,
            sticky="w",
            padx=8,
            pady=15,
        )

        ctk.CTkLabel(
            card,
            text="tasks",
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=2,
            padx=5,
        )

        ctk.CTkButton(
            card,
            text="Save Goal",
            width=105,
            height=36,
            corner_radius=9,
            font=("Segoe UI", 10, "bold"),
            command=self.save_goal,
        ).grid(
            row=0,
            column=3,
            padx=(10, 18),
        )

    # =========================================================
    # SAVE GOAL
    # =========================================================

    def save_goal(self):

        try:

            goal = max(
                1,
                int(
                    self.goal_var.get()
                ),
            )

        except ValueError:

            goal = 5

        data = load_study_data()

        data["daily_goal"] = goal

        save_study_data(
            data
        )

        self.goal_var.set(
            str(goal)
        )

        self.generate_plan()

    # =========================================================
    # SUMMARY
    # =========================================================

    def create_summary(self):

        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        for column in range(3):

            self.summary_frame.grid_columnconfigure(
                column,
                weight=1,
            )

    # =========================================================
    # SUMMARY CARD
    # =========================================================

    def create_summary_card(
        self,
        column,
        title,
        value,
        icon,
        accent,
        subtitle,
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
            corner_radius=17,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4,
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(13, 4),
        )

        icon_box = ctk.CTkFrame(
            top,
            width=32,
            height=32,
            corner_radius=8,
            fg_color=(
                "#F1F5F9",
                "#202A35",
            ),
        )

        icon_box.pack(
            side="left",
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Segoe UI", 14),
            text_color=accent,
        ).pack(
            expand=True,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=15,
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color=accent,
        ).pack(
            anchor="w",
            padx=15,
            pady=(1, 0),
        )

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 13),
        )

    # =========================================================
    # PLAN
    # =========================================================

    def create_plan(self):

        self.plan_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=18,
            fg_color=(
                "#F5F7FA",
                "#111820",
            ),
        )

        self.plan_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20),
        )

        self.plan_frame.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # GENERATE PLAN
    # =========================================================

    def generate_plan(self):

        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        for widget in self.plan_frame.winfo_children():
            widget.destroy()

        try:

            goal = max(
                1,
                int(
                    self.goal_var.get()
                ),
            )

        except ValueError:

            goal = 5

        self.goal_var.set(
            str(goal)
        )

        tasks = [
            task
            for task in load_tasks()
            if not task.get("completed")
        ]

        today = date.today()

        # -----------------------------------------------------
        # RANKING LOGIC
        # -----------------------------------------------------

        def ranking(task):

            priority_score = {
                "High": 3,
                "Medium": 2,
                "Low": 1,
            }.get(
                task.get("priority"),
                1,
            )

            difficulty_score = {
                "Hard": 3,
                "Medium": 2,
                "Easy": 1,
            }.get(
                task.get("difficulty"),
                1,
            )

            due_score = 0

            due = task.get(
                "due_date",
                "",
            )

            if due:

                try:

                    due_date = datetime.strptime(
                        due,
                        "%Y-%m-%d",
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
                100
                - get_task_progress(
                    task
                )
            ) / 100

            return (
                due_score
                + priority_score * 15
                + difficulty_score * 5
                + progress_score * 10
            )

        tasks.sort(
            key=ranking,
            reverse=True,
        )

        planned = tasks[:goal]

        total_minutes = sum(
            task.get(
                "estimated_minutes",
                30,
            )
            for task in planned
        )

        focus_blocks = max(
            1,
            round(
                total_minutes / 25
            ),
        )

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        self.create_summary_card(
            0,
            "TODAY'S PLAN",
            f"{len(planned)} tasks",
            "✓",
            "#3B82F6",
            "Recommended study workload",
        )

        self.create_summary_card(
            1,
            "ESTIMATED TIME",
            self.format_minutes(
                total_minutes
            ),
            "◷",
            "#8B5CF6",
            "Total planned study time",
        )

        self.create_summary_card(
            2,
            "FOCUS BLOCKS",
            str(focus_blocks),
            "🍅",
            "#F97316",
            "Approx. 25-minute sessions",
        )

        # -----------------------------------------------------
        # EMPTY STATE
        # -----------------------------------------------------

        if not planned:

            self.create_empty_plan()

            return

        # -----------------------------------------------------
        # PLAN HEADER
        # -----------------------------------------------------

        plan_header = ctk.CTkFrame(
            self.plan_frame,
            fg_color="transparent",
        )

        plan_header.pack(
            fill="x",
            padx=8,
            pady=(13, 8),
        )

        plan_header.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            plan_header,
            text="RECOMMENDED STUDY ORDER",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            plan_header,
            text=(
                "Prioritized using deadlines, priority, difficulty "
                "and current progress."
            ),
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0),
        )

        # -----------------------------------------------------
        # PLAN CARDS
        # -----------------------------------------------------

        for index, task in enumerate(
            planned,
            start=1,
        ):

            self.create_plan_card(
                index,
                task,
            )

    # =========================================================
    # EMPTY PLAN
    # =========================================================

    def create_empty_plan(self):

        empty = ctk.CTkFrame(
            self.plan_frame,
            corner_radius=20,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        empty.pack(
            fill="x",
            padx=8,
            pady=25,
        )

        ctk.CTkLabel(
            empty,
            text="✓",
            font=("Segoe UI", 42, "bold"),
            text_color=(
                "#22C55E",
                "#4ADE80",
            ),
        ).pack(
            pady=(35, 5),
        )

        ctk.CTkLabel(
            empty,
            text="Nothing is waiting on you",
            font=("Segoe UI", 21, "bold"),
        ).pack()

        ctk.CTkLabel(
            empty,
            text=(
                "Your pending task list is empty. "
                "Enjoy the breathing room or create a new task."
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            wraplength=600,
        ).pack(
            pady=(5, 30),
        )

    # =========================================================
    # PLAN CARD
    # =========================================================

    def create_plan_card(
        self,
        index,
        task,
    ):

        card = ctk.CTkFrame(
            self.plan_frame,
            corner_radius=17,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        card.pack(
            fill="x",
            padx=8,
            pady=5,
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # NUMBER
        # -----------------------------------------------------

        number_box = ctk.CTkFrame(
            card,
            width=42,
            height=42,
            corner_radius=12,
            fg_color=(
                "#EAF2FF",
                "#1B3554",
            ),
        )

        number_box.grid(
            row=0,
            column=0,
            rowspan=4,
            padx=(15, 10),
            pady=15,
        )

        number_box.grid_propagate(
            False
        )

        ctk.CTkLabel(
            number_box,
            text=str(index),
            font=("Segoe UI", 16, "bold"),
            text_color=(
                "#2563EB",
                "#60A5FA",
            ),
        ).pack(
            expand=True,
        )

        # -----------------------------------------------------
        # TASK NAME
        # -----------------------------------------------------

        ctk.CTkLabel(
            card,
            text=task.get(
                "task",
                "",
            ),
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=(14, 2),
        )

        # -----------------------------------------------------
        # DETAILS
        # -----------------------------------------------------

        detail = (
            f"{task.get('subject') or 'General'}"
            f"   •   "
            f"{task.get('priority', 'Medium')} priority"
            f"   •   "
            f"{task.get('difficulty', 'Medium')}"
            f"   •   "
            f"{task.get('estimated_minutes', 30)} min"
        )

        ctk.CTkLabel(
            card,
            text=detail,
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            anchor="w",
        ).grid(
            row=1,
            column=1,
            sticky="w",
        )

        # -----------------------------------------------------
        # REASON
        # -----------------------------------------------------

        reason = self.get_reason(
            task
        )

        ctk.CTkLabel(
            card,
            text=reason,
            font=("Segoe UI", 10, "bold"),
            text_color=self.get_reason_color(
                task
            ),
            anchor="w",
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(5, 1),
        )

        # -----------------------------------------------------
        # PROGRESS
        # -----------------------------------------------------

        progress = get_task_progress(
            task
        )

        progress_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        progress_frame.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=(4, 14),
        )

        progress_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        bar = ctk.CTkProgressBar(
            progress_frame,
            height=6,
            corner_radius=3,
            progress_color=(
                "#22C55E"
                if progress >= 100
                else "#3B82F6"
            ),
            fg_color=(
                "#E5E7EB",
                "#2A3441",
            ),
        )

        bar.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        bar.set(
            max(
                0,
                min(
                    1,
                    progress / 100,
                ),
            )
        )

        ctk.CTkLabel(
            progress_frame,
            text=f"{progress}%",
            width=40,
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=1,
            padx=(8, 0),
        )

        # -----------------------------------------------------
        # OPEN TASKS
        # -----------------------------------------------------

        ctk.CTkButton(
            card,
            text="Open Tasks",
            width=105,
            height=36,
            corner_radius=9,
            font=("Segoe UI", 10, "bold"),
            fg_color=(
                "#E8EEF6",
                "#263241",
            ),
            hover_color=(
                "#DCE5F0",
                "#314052",
            ),
            text_color=(
                "#334155",
                "#E2E8F0",
            ),
            command=self.app.show_tasks,
        ).grid(
            row=0,
            column=2,
            rowspan=4,
            padx=(12, 15),
        )

    # =========================================================
    # RECOMMENDATION REASON
    # =========================================================

    def get_reason(
        self,
        task,
    ):

        if (
            task.get("due_date")
            == date.today().isoformat()
        ):

            return "🔥 Recommended first — due today"

        if task.get("priority") == "High":

            return "⚡ Recommended first — high priority"

        if task.get("difficulty") == "Hard":

            return "🧠 Strong candidate for a focused study block"

        if task.get("starred"):

            return "⭐ Marked important — keep it on your radar"

        return "📚 Recommended from your current workload"

    # =========================================================
    # REASON COLOR
    # =========================================================

    def get_reason_color(
        self,
        task,
    ):

        if (
            task.get("due_date")
            == date.today().isoformat()
        ):

            return (
                "#DC2626"
                if ctk.get_appearance_mode()
                == "Light"
                else "#F87171"
            )

        if task.get("priority") == "High":

            return (
                "#D97706"
                if ctk.get_appearance_mode()
                == "Light"
                else "#FBBF24"
            )

        if task.get("difficulty") == "Hard":

            return (
                "#7C3AED"
                if ctk.get_appearance_mode()
                == "Light"
                else "#A78BFA"
            )

        return (
            "#2563EB"
            if ctk.get_appearance_mode()
            == "Light"
            else "#60A5FA"
        )

    # =========================================================
    # FORMAT MINUTES
    # =========================================================

    def format_minutes(
        self,
        minutes,
    ):

        minutes = int(
            minutes or 0
        )

        hours = minutes // 60

        remaining = minutes % 60

        if hours:

            if remaining:

                return (
                    f"{hours}h "
                    f"{remaining}m"
                )

            return f"{hours}h"

        return f"{remaining}m"