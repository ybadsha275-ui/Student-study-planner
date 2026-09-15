import customtkinter as ctk
from datetime import date, timedelta, datetime
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.task_manager import (
    load_tasks,
    load_study_data,
    get_task_progress,
    get_streak,
    get_due_status,
    get_statistics,
    get_subject_progress
)


class AnalyticsView(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.app = app

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.create_header()
        self.create_summary()
        self.create_content()

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
            text="Analytics",
            font=("Segoe UI", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Understand your study performance, workload and consistency.",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="Refresh Analytics",
            width=150,
            command=self.refresh
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10
        )

    # =========================================================
    # SUMMARY CARDS
    # =========================================================

    def create_summary(self):

        self.summary = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.summary.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=5
        )

        for column in range(6):

            self.summary.grid_columnconfigure(
                column,
                weight=1
            )

    def create_summary_card(
        self,
        column,
        title,
        value,
        subtitle=""
    ):

        card = ctk.CTkFrame(
            self.summary,
            corner_radius=15
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
            font=("Segoe UI", 10, "bold"),
            text_color=("gray45", "gray65")
        ).pack(
            pady=(12, 2)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=2
        )

        if subtitle:

            ctk.CTkLabel(
                card,
                text=subtitle,
                font=("Segoe UI", 9),
                text_color=("gray50", "gray65")
            ).pack(
                pady=(0, 12)
            )

    # =========================================================
    # CONTENT
    # =========================================================

    def create_content(self):

        self.content = ctk.CTkScrollableFrame(
            self,
            corner_radius=15
        )

        self.content.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 20)
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        for widget in self.summary.winfo_children():
            widget.destroy()

        for widget in self.content.winfo_children():
            widget.destroy()

        stats = get_statistics()

        streak = get_streak()

        study_data = load_study_data()

        total_focus = study_data.get(
            "total_focus_minutes",
            0
        )

        self.create_summary_card(
            0,
            "Total Tasks",
            stats["total"]
        )

        self.create_summary_card(
            1,
            "Completed",
            stats["completed"]
        )

        self.create_summary_card(
            2,
            "Pending",
            stats["pending"]
        )

        self.create_summary_card(
            3,
            "Completion",
            f"{stats['progress']}%"
        )

        self.create_summary_card(
            4,
            "Study Streak",
            f"{streak} days"
        )

        self.create_summary_card(
            5,
            "Focus Time",
            f"{total_focus} min"
        )

        self.create_task_statistics(stats)
        self.create_charts()
        self.create_heatmap()

    # =========================================================
    # TASK STATISTICS
    # =========================================================

    def create_task_statistics(
        self,
        stats
    ):

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Workload Overview",
            font=("Segoe UI", 19, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        rows = [
            (
                "Completed Tasks",
                stats["completed"]
            ),
            (
                "Pending Tasks",
                stats["pending"]
            ),
            (
                "Due Today",
                stats["today"]
            ),
            (
                "Overdue",
                stats["overdue"]
            ),
            (
                "Average Task Progress",
                f"{stats['average_progress']}%"
            ),
            (
                "Planned Study Time",
                self.format_minutes(
                    stats["total_planned_minutes"]
                )
            ),
            (
                "Remaining Study Time",
                self.format_minutes(
                    stats["estimated_minutes"]
                )
            )
        ]

        for title, value in rows:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=4
            )

            row.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                row,
                text=title,
                anchor="w",
                font=("Segoe UI", 12)
            ).grid(
                row=0,
                column=0,
                sticky="w"
            )

            ctk.CTkLabel(
                row,
                text=str(value),
                anchor="e",
                font=("Segoe UI", 12, "bold")
            ).grid(
                row=0,
                column=1,
                sticky="e"
            )

        ctk.CTkFrame(
            card,
            height=10,
            fg_color="transparent"
        ).pack()

    # =========================================================
    # CHARTS
    # =========================================================

    def create_charts(self):

        tasks = load_tasks()

        if not tasks:
            return

        chart_card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )

        chart_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            chart_card,
            text="Study Analytics Charts",
            font=("Segoe UI", 19, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        chart_frame = ctk.CTkFrame(
            chart_card,
            fg_color="transparent"
        )

        chart_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # -----------------------------------------------------
        # Chart 1: Status
        # -----------------------------------------------------

        status_counts = {
            "Completed": sum(
                1
                for task in tasks
                if task.get("completed")
            ),

            "Pending": sum(
                1
                for task in tasks
                if not task.get("completed")
            ),

            "Overdue": sum(
                1
                for task in tasks
                if get_due_status(task) == "Overdue"
                and not task.get("completed")
            )
        }

        figure1 = plt.Figure(
            figsize=(5.5, 3.6),
            dpi=90
        )

        ax1 = figure1.add_subplot(111)

        ax1.bar(
            list(status_counts.keys()),
            list(status_counts.values())
        )

        ax1.set_title(
            "Task Status"
        )

        ax1.set_ylabel(
            "Number of Tasks"
        )

        ax1.tick_params(
            axis="x",
            rotation=15
        )

        figure1.tight_layout()

        canvas1 = FigureCanvasTkAgg(
            figure1,
            master=chart_frame
        )

        canvas1.draw()

        canvas1.get_tk_widget().pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # -----------------------------------------------------
        # Chart 2: Priority
        # -----------------------------------------------------

        priority_counts = Counter(
            task.get(
                "priority",
                "Medium"
            )
            for task in tasks
        )

        figure2 = plt.Figure(
            figsize=(5.5, 3.6),
            dpi=90
        )

        ax2 = figure2.add_subplot(111)

        labels = list(
            priority_counts.keys()
        )

        values = list(
            priority_counts.values()
        )

        ax2.pie(
            values,
            labels=labels,
            autopct="%1.0f%%"
        )

        ax2.set_title(
            "Priority Distribution"
        )

        figure2.tight_layout()

        canvas2 = FigureCanvasTkAgg(
            figure2,
            master=chart_frame
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # -----------------------------------------------------
        # Chart 3: Subject Progress
        # -----------------------------------------------------

        subject_data = get_subject_progress()

        if subject_data:

            figure3 = plt.Figure(
                figsize=(10, 4),
                dpi=90
            )

            ax3 = figure3.add_subplot(111)

            subjects = list(
                subject_data.keys()
            )

            progress = [
                subject_data[subject]["progress"]
                for subject in subjects
            ]

            ax3.bar(
                subjects,
                progress
            )

            ax3.set_title(
                "Subject Completion Progress"
            )

            ax3.set_ylabel(
                "Progress (%)"
            )

            ax3.set_ylim(
                0,
                100
            )

            ax3.tick_params(
                axis="x",
                rotation=30
            )

            figure3.tight_layout()

            canvas3 = FigureCanvasTkAgg(
                figure3,
                master=chart_card
            )

            canvas3.draw()

            canvas3.get_tk_widget().pack(
                fill="x",
                padx=15,
                pady=10
            )

    # =========================================================
    # HEATMAP
    # =========================================================

    def create_heatmap(self):

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="30-Day Study Heatmap",
            font=("Segoe UI", 19, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            card,
            text="Each square represents one day of your recent study activity.",
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        heatmap = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        heatmap.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        tasks = load_tasks()
        study_data = load_study_data()

        study_dates = set(
            study_data.get(
                "study_dates",
                []
            )
        )

        # Task completions by date.
        completion_by_date = {}

        for task in tasks:

            completed_on = task.get(
                "completed_on",
                ""
            )

            if completed_on:

                completion_by_date[
                    completed_on
                ] = (
                    completion_by_date.get(
                        completed_on,
                        0
                    )
                    + 1
                )

        today = date.today()

        dates = [
            today - timedelta(
                days=offset
            )
            for offset in range(29, -1, -1)
        ]

        # 6 columns x 5 rows.
        for index, current_date in enumerate(dates):

            row = index // 10
            column = index % 10

            key = current_date.isoformat()

            completed_count = (
                completion_by_date.get(
                    key,
                    0
                )
            )

            focus_active = key in study_dates

            if completed_count == 0 and not focus_active:
                intensity = 0

            elif completed_count <= 1:
                intensity = 1

            elif completed_count <= 3:
                intensity = 2

            else:
                intensity = 3

            if intensity == 0:
                fg = ("gray86", "#252525")
            elif intensity == 1:
                fg = ("gray76", "#3a3a3a")
            elif intensity == 2:
                fg = ("gray62", "#555555")
            else:
                fg = ("gray45", "#707070")

            square = ctk.CTkFrame(
                heatmap,
                width=55,
                height=48,
                corner_radius=8,
                fg_color=fg
            )

            square.grid(
                row=row,
                column=column,
                padx=3,
                pady=3
            )

            square.grid_propagate(
                False
            )

            ctk.CTkLabel(
                square,
                text=current_date.strftime(
                    "%d"
                ),
                font=("Segoe UI", 10, "bold")
            ).pack(
                pady=(4, 0)
            )

            ctk.CTkLabel(
                square,
                text=str(
                    completed_count
                ),
                font=("Segoe UI", 9)
            ).pack()

        ctk.CTkLabel(
            card,
            text=(
                "Study activity is based on completed tasks "
                "and recorded focus sessions."
            ),
            font=("Segoe UI", 10),
            text_color=("gray50", "gray65")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    # =========================================================
    # FORMAT
    # =========================================================

    def format_minutes(
        self,
        minutes
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