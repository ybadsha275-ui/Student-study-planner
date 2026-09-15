import customtkinter as ctk

from tkinter import messagebox
from datetime import datetime

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
    sort_tasks,
)

from core.gamification import (
    load_gamification,
    award_task_xp,
    check_achievements,
    get_level,
    get_achievement_definitions,
)


class TasksView(ctk.CTkFrame):

    def __init__(self, master, app):

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
        # FILTER VARIABLES
        # =====================================================

        self.search_var = ctk.StringVar(value="")
        self.priority_var = ctk.StringVar(value="All")
        self.status_var = ctk.StringVar(value="All")
        self.category_var = ctk.StringVar(value="All")
        self.difficulty_var = ctk.StringVar(value="All")
        self.sort_var = ctk.StringVar(value="Default")
        self.starred_var = ctk.BooleanVar(value=False)

        # =====================================================
        # LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            2,
            weight=1,
        )

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
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 12),
        )

        header.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # LEFT SIDE
        # -----------------------------------------------------

        heading = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        heading.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            heading,
            text="TASK MANAGEMENT",
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
            text="My Tasks",
            font=("Segoe UI", 29, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            heading,
            text=(
                "Organize your study work, track progress "
                "and stay ahead of deadlines."
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
        # RIGHT SIDE
        # -----------------------------------------------------

        ctk.CTkButton(
            header,
            text="＋  Add Task",
            width=145,
            height=44,
            corner_radius=11,
            font=("Segoe UI", 12, "bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.open_add_dialog,
        ).grid(
            row=0,
            column=1,
            padx=(15, 0),
        )

    # =========================================================
    # FILTERS
    # =========================================================

    def create_filters(self):

        card = ctk.CTkFrame(
            self,
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
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        card.grid_columnconfigure(
            0,
            weight=2,
        )

        for column in range(1, 7):
            card.grid_columnconfigure(
                column,
                weight=1,
            )

        # -----------------------------------------------------
        # FILTER TITLE
        # -----------------------------------------------------

        ctk.CTkLabel(
            card,
            text="FILTERS",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=0,
            columnspan=7,
            sticky="w",
            padx=14,
            pady=(11, 2),
        )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        search_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        search_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=7,
            pady=(2, 12),
        )

        search_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            search_frame,
            text="⌕",
            font=("Segoe UI Symbol", 18),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=0,
            padx=(4, 5),
        )

        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search task, subject, category or description...",
            height=38,
            corner_radius=10,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
        )

        search_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # COMBO BOXES
        # -----------------------------------------------------

        self.make_combo(
            card,
            self.priority_var,
            ["All", "High", "Medium", "Low"],
            1,
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
                "No Due Date",
            ],
            2,
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
                "Other",
            ],
            3,
        )

        self.make_combo(
            card,
            self.difficulty_var,
            [
                "All",
                "Easy",
                "Medium",
                "Hard",
            ],
            4,
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
                "Name",
            ],
            5,
        )

        # -----------------------------------------------------
        # STARRED
        # -----------------------------------------------------

        ctk.CTkCheckBox(
            card,
            text="★ Starred",
            variable=self.starred_var,
            command=self.refresh,
            font=("Segoe UI", 11, "bold"),
            height=34,
        ).grid(
            row=1,
            column=6,
            padx=6,
            pady=(2, 12),
        )

        # -----------------------------------------------------
        # CLEAR BUTTON
        # -----------------------------------------------------

        ctk.CTkButton(
            card,
            text="Clear",
            width=72,
            height=34,
            corner_radius=9,
            font=("Segoe UI", 10, "bold"),
            fg_color=(
                "#E8ECF1",
                "#293442",
            ),
            hover_color=(
                "#DCE2E9",
                "#344150",
            ),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
            command=self.clear_filters,
        ).grid(
            row=1,
            column=7,
            padx=(0, 10),
            pady=(2, 12),
        )

        # -----------------------------------------------------
        # AUTO REFRESH FILTERS
        # -----------------------------------------------------

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

        self.priority_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

        self.status_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

        self.category_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

        self.difficulty_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

        self.sort_var.trace_add(
            "write",
            lambda *_: self.refresh(),
        )

    # =========================================================
    # COMBO BOX
    # =========================================================

    def make_combo(
        self,
        parent,
        variable,
        values,
        column,
    ):

        ctk.CTkComboBox(
            parent,
            variable=variable,
            values=values,
            height=36,
            corner_radius=9,
            font=("Segoe UI", 10),
        ).grid(
            row=1,
            column=column,
            padx=5,
            pady=(2, 12),
            sticky="ew",
        )

    # =========================================================
    # TASK LIST
    # =========================================================

    def create_task_list(self):

        self.task_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )

        self.task_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20),
        )

        self.task_list.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        for widget in self.task_list.winfo_children():

            widget.destroy()

        tasks = load_tasks()

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        query = self.search_var.get().strip().lower()

        if query:

            tasks = [
                task
                for task in tasks
                if query in task.get(
                    "task",
                    "",
                ).lower()
                or query in task.get(
                    "subject",
                    "",
                ).lower()
                or query in task.get(
                    "description",
                    "",
                ).lower()
                or query in task.get(
                    "category",
                    "",
                ).lower()
            ]

        # -----------------------------------------------------
        # FILTERS
        # -----------------------------------------------------

        tasks = filter_tasks(
            tasks,
            priority=self.priority_var.get(),
            status=self.status_var.get(),
            category=self.category_var.get(),
            difficulty=self.difficulty_var.get(),
            starred=self.starred_var.get(),
        )

        # -----------------------------------------------------
        # SORT
        # -----------------------------------------------------

        tasks = sort_tasks(
            tasks,
            self.sort_var.get(),
        )

        # -----------------------------------------------------
        # RESULT HEADER
        # -----------------------------------------------------

        result_bar = ctk.CTkFrame(
            self.task_list,
            fg_color="transparent",
        )

        result_bar.pack(
            fill="x",
            padx=4,
            pady=(0, 7),
        )

        ctk.CTkLabel(
            result_bar,
            text=(
                f"{len(tasks)} task"
                f"{'' if len(tasks) == 1 else 's'}"
            ),
            font=("Segoe UI", 11, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
        )

        if self.starred_var.get():

            ctk.CTkLabel(
                result_bar,
                text="★ Starred filter active",
                font=("Segoe UI", 10, "bold"),
                text_color=(
                    "#A16207",
                    "#FBBF24",
                ),
            ).pack(
                side="right",
            )

        # -----------------------------------------------------
        # EMPTY STATE
        # -----------------------------------------------------

        if not tasks:

            self.create_empty_state()
            return

        # -----------------------------------------------------
        # TASK CARDS
        # -----------------------------------------------------

        for task in tasks:

            self.create_task_card(
                task
            )

    # =========================================================
    # EMPTY STATE
    # =========================================================

    def create_empty_state(self):

        empty = ctk.CTkFrame(
            self.task_list,
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
            pady=18,
        )

        ctk.CTkLabel(
            empty,
            text="✓",
            font=("Segoe UI", 38, "bold"),
            text_color=(
                "#3B82F6",
                "#60A5FA",
            ),
        ).pack(
            pady=(35, 8),
        )

        ctk.CTkLabel(
            empty,
            text="No tasks found",
            font=("Segoe UI", 20, "bold"),
        ).pack()

        ctk.CTkLabel(
            empty,
            text=(
                "Try adjusting your filters or create "
                "a new study task."
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            pady=(5, 5),
        )

        ctk.CTkButton(
            empty,
            text="＋ Create First Task",
            width=160,
            height=38,
            corner_radius=10,
            command=self.open_add_dialog,
        ).pack(
            pady=(13, 35),
        )

    # =========================================================
    # TASK CARD
    # =========================================================

    def create_task_card(
        self,
        task,
    ):

        card = ctk.CTkFrame(
            self.task_list,
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
            padx=4,
            pady=6,
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # COMPLETION CHECKBOX
        # -----------------------------------------------------

        checkbox = ctk.CTkCheckBox(
            card,
            text="",
            width=24,
            height=24,
            corner_radius=7,
            border_width=2,
            command=lambda task_id=task["id"]:
            self.complete_task(task_id),
        )

        checkbox.grid(
            row=0,
            column=0,
            rowspan=6,
            padx=(16, 5),
            pady=17,
            sticky="n",
        )

        if task.get("completed"):

            checkbox.select()

        # -----------------------------------------------------
        # MAIN CONTENT
        # -----------------------------------------------------

        content = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        content.grid(
            row=0,
            column=1,
            rowspan=6,
            sticky="ew",
            padx=8,
            pady=13,
        )

        content.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # TITLE ROW
        # -----------------------------------------------------

        title_row = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )

        title_row.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        title_row.grid_columnconfigure(
            0,
            weight=1,
        )

        title = task.get(
            "task",
            "Untitled Task",
        )

        title_color = (
            self.colors["muted_light"]
            if task.get("completed")
            else (
                self.colors["text_light"]
                if ctk.get_appearance_mode() == "Light"
                else self.colors["text_dark"]
            )
        )

        ctk.CTkLabel(
            title_row,
            text=title,
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            text_color=title_color,
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        # Star
        star_text = (
            "★"
            if task.get("starred", False)
            else "☆"
        )

        ctk.CTkButton(
            title_row,
            text=star_text,
            width=34,
            height=30,
            corner_radius=8,
            font=("Segoe UI Symbol", 17),
            fg_color="transparent",
            hover_color=(
                "#F3F4F6",
                "#252F3B",
            ),
            text_color=(
                "#A16207",
                "#FBBF24",
            ),
            command=lambda task_id=task["id"]:
            self.star_task(task_id),
        ).grid(
            row=0,
            column=1,
            padx=(5, 0),
        )

        # -----------------------------------------------------
        # BADGES
        # -----------------------------------------------------

        badges = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )

        badges.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(6, 4),
        )

        self.create_badge(
            badges,
            task.get(
                "priority",
                "Medium",
            ),
            self.get_priority_color(
                task.get(
                    "priority",
                    "Medium",
                )
            ),
        )

        self.create_badge(
            badges,
            task.get(
                "difficulty",
                "Medium",
            ),
            self.get_difficulty_color(
                task.get(
                    "difficulty",
                    "Medium",
                )
            ),
        )

        self.create_badge(
            badges,
            task.get(
                "category",
                "Study",
            ),
            "#64748B",
        )

        # -----------------------------------------------------
        # INFO
        # -----------------------------------------------------

        subject = task.get(
            "subject",
            "",
        ) or "No subject"

        estimated = task.get(
            "estimated_minutes",
            30,
        )

        info = (
            f"{subject}   •   "
            f"{estimated} min study time"
        )

        ctk.CTkLabel(
            content,
            text=info,
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            anchor="w",
        ).grid(
            row=2,
            column=0,
            sticky="w",
        )

        # -----------------------------------------------------
        # DUE DATE
        # -----------------------------------------------------

        due_text = self.get_due_text(
            task
        )

        due_status = get_due_status(
            task
        )

        due_color = self.get_due_color(
            due_status
        )

        ctk.CTkLabel(
            content,
            text=due_text,
            font=("Segoe UI", 10, "bold"),
            text_color=due_color,
            anchor="w",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(4, 6),
        )

        # -----------------------------------------------------
        # PROGRESS
        # -----------------------------------------------------

        progress = get_task_progress(
            task
        )

        progress_frame = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )

        progress_frame.grid(
            row=4,
            column=0,
            sticky="ew",
        )

        progress_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        bar = ctk.CTkProgressBar(
            progress_frame,
            height=8,
            corner_radius=4,
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
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            width=42,
        ).grid(
            row=0,
            column=1,
            padx=(8, 0),
        )

        # -----------------------------------------------------
        # SUBTASK SUMMARY
        # -----------------------------------------------------

        subtasks = task.get(
            "subtasks",
            [],
        )

        if subtasks:

            done = sum(
                1
                for subtask in subtasks
                if subtask.get(
                    "completed",
                    False,
                )
            )

            subtask_text = (
                f"☑  {done}/{len(subtasks)} subtasks completed"
            )

        else:

            subtask_text = (
                "No subtasks"
            )

        ctk.CTkLabel(
            content,
            text=subtask_text,
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            anchor="w",
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=(5, 2),
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        actions.grid(
            row=0,
            column=2,
            rowspan=6,
            padx=(10, 14),
            pady=13,
            sticky="n",
        )

        # Edit
        self.action_button(
            actions,
            "Edit",
            lambda task_id=task["id"]:
            self.open_edit_dialog(task_id),
        ).pack(
            pady=(0, 5),
        )

        # Delete
        self.action_button(
            actions,
            "Delete",
            lambda task_id=task["id"]:
            self.remove_task(task_id),
            danger=True,
        ).pack(
            pady=0,
        )

        # -----------------------------------------------------
        # SUBTASK DETAILS
        # -----------------------------------------------------

        if subtasks:

            self.create_subtask_section(
                task,
                subtasks,
            )

    # =========================================================
    # BADGE
    # =========================================================

    def create_badge(
        self,
        parent,
        text,
        accent,
    ):

        badge = ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            corner_radius=7,
            fg_color=(
                "#F1F5F9",
                "#202A36",
            ),
            text_color=accent,
            padx=8,
            pady=3,
        )

        badge.pack(
            side="left",
            padx=(0, 5),
        )

    # =========================================================
    # ACTION BUTTON
    # =========================================================

    def action_button(
        self,
        parent,
        text,
        command,
        danger=False,
    ):

        if danger:

            return ctk.CTkButton(
                parent,
                text=text,
                width=68,
                height=31,
                corner_radius=8,
                font=("Segoe UI", 10, "bold"),
                fg_color=(
                    "#FEE2E2",
                    "#512323",
                ),
                hover_color=(
                    "#FECACA",
                    "#682A2A",
                ),
                text_color=(
                    "#B91C1C",
                    "#FCA5A5",
                ),
                command=command,
            )

        return ctk.CTkButton(
            parent,
            text=text,
            width=68,
            height=31,
            corner_radius=8,
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
            command=command,
        )

    # =========================================================
    # SUBTASK SECTION
    # =========================================================

    def create_subtask_section(
        self,
        task,
        subtasks,
    ):

        section = ctk.CTkFrame(
            self.task_list,
            corner_radius=13,
            fg_color=(
                "#F7F8FA",
                "#151D26",
            ),
            border_width=1,
            border_color=(
                "#E6EAF0",
                "#222D38",
            ),
        )

        section.pack(
            fill="x",
            padx=20,
            pady=(0, 7),
        )

        header = ctk.CTkFrame(
            section,
            fg_color="transparent",
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(9, 4),
        )

        ctk.CTkLabel(
            header,
            text="SUBTASKS",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
        )

        ctk.CTkLabel(
            header,
            text=task.get(
                "task",
                "",
            ),
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        ).pack(
            side="right",
        )

        for subtask in subtasks:

            variable = ctk.BooleanVar(
                value=subtask.get(
                    "completed",
                    False,
                )
            )

            ctk.CTkCheckBox(
                section,
                text=subtask.get(
                    "text",
                    "",
                ),
                variable=variable,
                font=("Segoe UI", 10),
                command=lambda
                task_id=task["id"],
                subtask_id=subtask["id"]:
                self.change_subtask(
                    task_id,
                    subtask_id,
                ),
            ).pack(
                anchor="w",
                padx=15,
                pady=3,
            )

        ctk.CTkFrame(
            section,
            height=6,
            fg_color="transparent",
        ).pack()

    # =========================================================
    # PRIORITY COLOR
    # =========================================================

    def get_priority_color(
        self,
        priority,
    ):

        colors = {
            "High": (
                "#DC2626",
                "#F87171",
            ),
            "Medium": (
                "#D97706",
                "#FBBF24",
            ),
            "Low": (
                "#15803D",
                "#4ADE80",
            ),
        }

        light, dark = colors.get(
            priority,
            (
                "#64748B",
                "#94A3B8",
            ),
        )

        return (
            light
            if ctk.get_appearance_mode() == "Light"
            else dark
        )

    # =========================================================
    # DIFFICULTY COLOR
    # =========================================================

    def get_difficulty_color(
        self,
        difficulty,
    ):

        colors = {
            "Hard": (
                "#7C3AED",
                "#A78BFA",
            ),
            "Medium": (
                "#2563EB",
                "#60A5FA",
            ),
            "Easy": (
                "#0891B2",
                "#67E8F9",
            ),
        }

        light, dark = colors.get(
            difficulty,
            (
                "#64748B",
                "#94A3B8",
            ),
        )

        return (
            light
            if ctk.get_appearance_mode() == "Light"
            else dark
        )

    # =========================================================
    # DUE COLOR
    # =========================================================

    def get_due_color(
        self,
        status,
    ):

        colors = {
            "Overdue": (
                "#DC2626",
                "#F87171",
            ),
            "Due Today": (
                "#D97706",
                "#FBBF24",
            ),
            "Completed": (
                "#15803D",
                "#4ADE80",
            ),
        }

        light, dark = colors.get(
            status,
            (
                "#64748B",
                "#94A3B8",
            ),
        )

        return (
            light
            if ctk.get_appearance_mode() == "Light"
            else dark
        )

    # =========================================================
    # COMPLETE TASK
    # =========================================================

    def complete_task(
        self,
        task_id,
    ):

        old_task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None,
        )

        if old_task is None:

            return

        was_completed = bool(
            old_task.get(
                "completed",
                False,
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
                False,
            )
        ):

            self.handle_task_xp(
                updated_task
            )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard",
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # SUBTASK
    # =========================================================

    def change_subtask(
        self,
        task_id,
        subtask_id,
    ):

        old_task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None,
        )

        was_completed = (
            bool(
                old_task.get(
                    "completed",
                    False,
                )
            )
            if old_task
            else False
        )

        updated_task = toggle_subtask(
            task_id,
            subtask_id,
        )

        if (
            updated_task
            and not was_completed
            and updated_task.get(
                "completed",
                False,
            )
        ):

            self.handle_task_xp(
                updated_task
            )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard",
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # XP
    # =========================================================

    def handle_task_xp(
        self,
        task,
    ):

        before = load_gamification()

        old_xp = int(
            before.get(
                "xp",
                0,
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
                0,
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
                message,
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
                message,
            )

        else:

            self.show_game_notification(
                "⭐ XP Earned",
                f"+{earned} XP",
            )

    # =========================================================
    # ACHIEVEMENT NAMES
    # =========================================================

    def get_achievement_names(
        self,
        achievement_ids,
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
        message,
    ):

        notification = ctk.CTkToplevel(
            self
        )

        notification.title(
            title
        )

        notification.geometry(
            "390x225"
        )

        notification.resizable(
            False,
            False
        )

        notification.transient(
            self
        )

        notification.grab_set()

        card = ctk.CTkFrame(
            notification,
            corner_radius=18,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
        )

        card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 19, "bold"),
        ).pack(
            pady=(22, 8)
        )

        ctk.CTkLabel(
            card,
            text=message,
            font=("Segoe UI", 12),
            justify="center",
            wraplength=325,
        ).pack(
            padx=15
        )

        ctk.CTkButton(
            card,
            text="Nice!",
            width=110,
            height=36,
            corner_radius=10,
            command=notification.destroy,
        ).pack(
            pady=15
        )

        notification.after(
            5000,
            lambda: (
                notification.destroy()
                if notification.winfo_exists()
                else None
            ),
        )

    # =========================================================
    # STAR
    # =========================================================

    def star_task(
        self,
        task_id,
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
        task_id,
    ):

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to permanently delete this task?",
        )

        if not confirm:

            return

        delete_task(
            task_id
        )

        self.refresh()

        if hasattr(
            self.app,
            "refresh_dashboard",
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # FILTER RESET
    # =========================================================

    def clear_filters(self):

        self.search_var.set("")

        self.priority_var.set(
            "All"
        )

        self.status_var.set(
            "All"
        )

        self.category_var.set(
            "All"
        )

        self.difficulty_var.set(
            "All"
        )

        self.sort_var.set(
            "Default"
        )

        self.starred_var.set(
            False
        )

    # =========================================================
    # DUE DATE
    # =========================================================

    def get_due_text(
        self,
        task,
    ):

        status = get_due_status(
            task
        )

        due_date = task.get(
            "due_date",
            "",
        )

        if not due_date:

            return "No due date"

        if status == "Completed":

            return f"✓ Completed  •  {due_date}"

        if status == "Overdue":

            return f"⚠ OVERDUE  •  {due_date}"

        if status == "Due Today":

            return f"● DUE TODAY  •  {due_date}"

        return f"Due  •  {due_date}"

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
        task_id,
    ):

        task = next(
            (
                task
                for task in load_tasks()
                if task.get("id") == task_id
            ),
            None,
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
        task=None,
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
            "680x800"
        )

        dialog.minsize(
            620,
            700,
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        # -----------------------------------------------------
        # DIALOG CONTAINER
        # -----------------------------------------------------

        container = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent",
        )

        container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18,
        )

        container.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # DIALOG HEADER
        # -----------------------------------------------------

        header = ctk.CTkFrame(
            container,
            corner_radius=16,
            fg_color=(
                "#EAF2FF",
                "#16243A",
            ),
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        ctk.CTkLabel(
            header,
            text=(
                "EDIT TASK"
                if is_edit
                else "NEW TASK"
            ),
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 2),
        )

        ctk.CTkLabel(
            header,
            text=(
                "Update your study task details."
                if is_edit
                else "Create a structured task for your study plan."
            ),
            font=("Segoe UI", 12),
            text_color=(
                "#526174",
                "#A8B4C4",
            ),
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 15),
        )

        # -----------------------------------------------------
        # VARIABLES
        # -----------------------------------------------------

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
                    "Medium",
                )
                if is_edit
                else "Medium"
            )
        )

        category_var = ctk.StringVar(
            value=(
                task.get(
                    "category",
                    "Study",
                )
                if is_edit
                else "Study"
            )
        )

        difficulty_var = ctk.StringVar(
            value=(
                task.get(
                    "difficulty",
                    "Medium",
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
                        30,
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
                    "",
                )
                if is_edit
                else ""
            )
        )

        recurring_var = ctk.StringVar(
            value=(
                task.get(
                    "recurring",
                    "None",
                )
                if is_edit
                else "None"
            )
        )

        # -----------------------------------------------------
        # FORM CARD
        # -----------------------------------------------------

        form = ctk.CTkFrame(
            container,
            corner_radius=16,
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

        form.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        form.grid_columnconfigure(
            1,
            weight=1,
        )

        def add_label(
            text,
            row,
        ):

            ctk.CTkLabel(
                form,
                text=text,
                font=("Segoe UI", 11, "bold"),
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(18, 10),
                pady=8,
            )

        def add_entry(
            variable,
            row,
            placeholder="",
        ):

            entry = ctk.CTkEntry(
                form,
                textvariable=variable,
                placeholder_text=placeholder,
                height=36,
                corner_radius=9,
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=(0, 18),
                pady=8,
            )

            return entry

        # -----------------------------------------------------
        # BASIC DETAILS
        # -----------------------------------------------------

        add_label(
            "Task Name",
            0,
        )

        add_entry(
            task_var,
            0,
            "e.g. Practice Java DSA",
        )

        add_label(
            "Subject",
            1,
        )

        add_entry(
            subject_var,
            1,
            "e.g. Java",
        )

        add_label(
            "Priority",
            2,
        )

        ctk.CTkComboBox(
            form,
            variable=priority_var,
            values=[
                "High",
                "Medium",
                "Low",
            ],
            height=36,
            corner_radius=9,
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(0, 18),
            pady=8,
        )

        add_label(
            "Category",
            3,
        )

        ctk.CTkComboBox(
            form,
            variable=category_var,
            values=[
                "Study",
                "Assignment",
                "Exam",
                "Project",
                "Revision",
                "Other",
            ],
            height=36,
            corner_radius=9,
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(0, 18),
            pady=8,
        )

        add_label(
            "Difficulty",
            4,
        )

        ctk.CTkComboBox(
            form,
            variable=difficulty_var,
            values=[
                "Easy",
                "Medium",
                "Hard",
            ],
            height=36,
            corner_radius=9,
        ).grid(
            row=4,
            column=1,
            sticky="ew",
            padx=(0, 18),
            pady=8,
        )

        add_label(
            "Study Time",
            5,
        )

        minutes_entry = add_entry(
            minutes_var,
            5,
            "Minutes",
        )

        add_label(
            "Due Date",
            6,
        )

        add_entry(
            due_var,
            6,
            "YYYY-MM-DD",
        )

        ctk.CTkLabel(
            form,
            text="Example: 2026-09-20",
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=7,
            column=1,
            sticky="w",
            padx=(0, 18),
            pady=(0, 5),
        )

        add_label(
            "Recurring",
            8,
        )

        ctk.CTkComboBox(
            form,
            variable=recurring_var,
            values=[
                "None",
                "Daily",
                "Weekly",
                "Monthly",
            ],
            height=36,
            corner_radius=9,
        ).grid(
            row=8,
            column=1,
            sticky="ew",
            padx=(0, 18),
            pady=8,
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        description_header = ctk.CTkLabel(
            container,
            text="DESCRIPTION",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        )

        description_header.grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=(17, 5),
        )

        description_box = ctk.CTkTextbox(
            container,
            height=115,
            corner_radius=12,
        )

        description_box.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=2,
        )

        if is_edit:

            description_box.insert(
                "1.0",
                task.get(
                    "description",
                    "",
                ),
            )

        # -----------------------------------------------------
        # SUBTASKS
        # -----------------------------------------------------

        subtask_header = ctk.CTkLabel(
            container,
            text="SUBTASKS",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        )

        subtask_header.grid(
            row=4,
            column=0,
            sticky="w",
            padx=5,
            pady=(17, 5),
        )

        ctk.CTkLabel(
            container,
            text="Add one subtask per line.",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=5,
            pady=(0, 5),
        )

        subtasks_box = ctk.CTkTextbox(
            container,
            height=150,
            corner_radius=12,
        )

        subtasks_box.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=2,
        )

        if is_edit:

            for subtask in task.get(
                "subtasks",
                [],
            ):

                subtasks_box.insert(
                    "end",
                    subtask.get(
                        "text",
                        "",
                    )
                    + "\n",
                )

        # -----------------------------------------------------
        # SAVE
        # -----------------------------------------------------

        def save():

            name = task_var.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Task",
                    "Please enter a task name.",
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
                    "Study time must be a positive number.",
                )

                return

            due_date = due_var.get().strip()

            if due_date:

                try:

                    datetime.strptime(
                        due_date,
                        "%Y-%m-%d",
                    )

                except ValueError:

                    messagebox.showwarning(
                        "Invalid Date",
                        "Use YYYY-MM-DD format.",
                    )

                    return

            description = description_box.get(
                "1.0",
                "end",
            ).strip()

            subtask_lines = [
                line.strip()
                for line in subtasks_box.get(
                    "1.0",
                    "end",
                ).splitlines()
                if line.strip()
            ]

            # -------------------------------------------------
            # EDIT
            # -------------------------------------------------

            if is_edit:

                old_subtasks = {
                    item.get("text"): item
                    for item in task.get(
                        "subtasks",
                        [],
                    )
                }

                processed = []

                for text in subtask_lines:

                    old = old_subtasks.get(
                        text
                    )

                    processed.append(
                        {
                            "id": (
                                old.get("id")
                                if old
                                else None
                            ),
                            "text": text,
                            "completed": (
                                old.get(
                                    "completed",
                                    False,
                                )
                                if old
                                else False
                            ),
                        }
                    )

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
                    subtasks=processed,
                )

            # -------------------------------------------------
            # ADD
            # -------------------------------------------------

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
                    subtasks=subtask_lines,
                )

            dialog.destroy()

            self.refresh()

            if hasattr(
                self.app,
                "refresh_dashboard",
            ):

                self.app.refresh_dashboard()

        # -----------------------------------------------------
        # DIALOG BUTTONS
        # -----------------------------------------------------

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent",
        )

        buttons.pack(
            fill="x",
            padx=18,
            pady=(0, 18),
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=120,
            height=40,
            corner_radius=10,
            fg_color=(
                "#E8ECF1",
                "#293442",
            ),
            hover_color=(
                "#DCE2E9",
                "#344150",
            ),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
            command=dialog.destroy,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            buttons,
            text=(
                "Save Changes"
                if is_edit
                else "Create Task"
            ),
            width=145,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 11, "bold"),
            command=save,
        ).pack(
            side="right",
            padx=5,
        )

        # -----------------------------------------------------
        # KEYBOARD SHORTCUTS
        # -----------------------------------------------------

        dialog.bind(
            "<Escape>",
            lambda event: dialog.destroy(),
        )

        dialog.bind(
            "<Control-Return>",
            lambda event: save(),
        )

        dialog.after(
            100,
            dialog.focus_force,
        )