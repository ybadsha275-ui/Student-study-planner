import customtkinter as ctk

from datetime import date, timedelta
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.task_manager import (
    load_tasks,
    load_study_data,
    get_streak,
    get_due_status,
    get_statistics,
    get_subject_progress,
)


class AnalyticsView(ctk.CTkFrame):

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
            2,
            weight=1,
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
        # TITLE
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
            text="PERFORMANCE INSIGHTS",
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
            text="Analytics",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            heading,
            text=(
                "Understand your study performance, workload "
                "and consistency."
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
        # REFRESH BUTTON
        # -----------------------------------------------------

        ctk.CTkButton(
            header,
            text="↻  Refresh Analytics",
            width=155,
            height=42,
            corner_radius=11,
            font=("Segoe UI", 11, "bold"),
            command=self.refresh,
        ).grid(
            row=0,
            column=1,
            padx=(15, 0),
        )

    # =========================================================
    # SUMMARY
    # =========================================================

    def create_summary(self):

        self.summary = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.summary.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        for column in range(6):

            self.summary.grid_columnconfigure(
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
        subtitle="",
        accent="#3B82F6",
        icon="",
    ):

        card = ctk.CTkFrame(
            self.summary,
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
            padx=13,
            pady=(12, 4),
        )

        icon_box = ctk.CTkFrame(
            top,
            width=31,
            height=31,
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
            font=("Segoe UI", 13, "bold"),
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
            padx=13,
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 24, "bold"),
            text_color=accent,
        ).pack(
            anchor="w",
            padx=13,
            pady=(1, 0),
        )

        if subtitle:

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
                padx=13,
                pady=(0, 12),
            )

    # =========================================================
    # CONTENT
    # =========================================================

    def create_content(self):

        self.content = ctk.CTkScrollableFrame(
            self,
            corner_radius=18,
            fg_color=(
                "#F5F7FA",
                "#111820",
            ),
        )

        self.content.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20),
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        # Clear summary.
        for widget in self.summary.winfo_children():
            widget.destroy()

        # Clear content.
        for widget in self.content.winfo_children():
            widget.destroy()

        stats = get_statistics()

        streak = get_streak()

        study_data = load_study_data()

        total_focus = study_data.get(
            "total_focus_minutes",
            0,
        )

        # -----------------------------------------------------
        # SUMMARY CARDS
        # -----------------------------------------------------

        self.create_summary_card(
            0,
            "TOTAL TASKS",
            stats["total"],
            "All planned work",
            "#3B82F6",
            "📚",
        )

        self.create_summary_card(
            1,
            "COMPLETED",
            stats["completed"],
            "Finished tasks",
            "#22C55E",
            "✓",
        )

        self.create_summary_card(
            2,
            "PENDING",
            stats["pending"],
            "Still remaining",
            "#F59E0B",
            "◷",
        )

        self.create_summary_card(
            3,
            "COMPLETION",
            f"{stats['progress']}%",
            "Overall progress",
            "#8B5CF6",
            "↗",
        )

        self.create_summary_card(
            4,
            "STUDY STREAK",
            f"{streak} days",
            "Consistency",
            "#F97316",
            "🔥",
        )

        self.create_summary_card(
            5,
            "FOCUS TIME",
            f"{total_focus} min",
            "Recorded focus",
            "#0891B2",
            "🧠",
        )

        # -----------------------------------------------------
        # MAIN SECTIONS
        # -----------------------------------------------------

        self.create_task_statistics(
            stats
        )

        self.create_charts()

        self.create_heatmap()

    # =========================================================
    # SECTION CARD
    # =========================================================

    def create_section_card(
        self,
    ):

        return ctk.CTkFrame(
            self.content,
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

    # =========================================================
    # SECTION HEADER
    # =========================================================

    def create_section_header(
        self,
        parent,
        title,
        subtitle,
        icon,
    ):

        heading = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        heading.pack(
            fill="x",
            padx=20,
            pady=(17, 4),
        )

        ctk.CTkLabel(
            heading,
            text=icon,
            font=("Segoe UI", 18),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        text_frame = ctk.CTkFrame(
            heading,
            fg_color="transparent",
        )

        text_frame.pack(
            side="left",
        )

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Segoe UI", 17, "bold"),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            text_frame,
            text=subtitle,
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            pady=(1, 0),
        )

    # =========================================================
    # TASK STATISTICS
    # =========================================================

    def create_task_statistics(
        self,
        stats,
    ):

        card = self.create_section_card()

        card.pack(
            fill="x",
            padx=10,
            pady=(0, 12),
        )

        self.create_section_header(
            card,
            "Workload Overview",
            "A quick breakdown of your current academic workload.",
            "◈",
        )

        rows = [
            (
                "Completed Tasks",
                stats["completed"],
                "#22C55E",
            ),
            (
                "Pending Tasks",
                stats["pending"],
                "#F59E0B",
            ),
            (
                "Due Today",
                stats["today"],
                "#3B82F6",
            ),
            (
                "Overdue",
                stats["overdue"],
                "#EF4444",
            ),
            (
                "Average Task Progress",
                f"{stats['average_progress']}%",
                "#8B5CF6",
            ),
            (
                "Planned Study Time",
                self.format_minutes(
                    stats["total_planned_minutes"]
                ),
                "#0891B2",
            ),
            (
                "Remaining Study Time",
                self.format_minutes(
                    stats["estimated_minutes"]
                ),
                "#7C3AED",
            ),
        ]

        for index, (
            title,
            value,
            accent,
        ) in enumerate(rows):

            row = ctk.CTkFrame(
                card,
                corner_radius=10,
                fg_color=(
                    "#F7F8FA",
                    "#202832",
                ),
            )

            row.pack(
                fill="x",
                padx=20,
                pady=3,
            )

            ctk.CTkLabel(
                row,
                text=title,
                anchor="w",
                font=("Segoe UI", 11),
            ).pack(
                side="left",
                padx=13,
                pady=9,
            )

            ctk.CTkLabel(
                row,
                text=str(value),
                anchor="e",
                font=("Segoe UI", 11, "bold"),
                text_color=accent,
            ).pack(
                side="right",
                padx=13,
            )

        ctk.CTkFrame(
            card,
            height=7,
            fg_color="transparent",
        ).pack()

    # =========================================================
    # CHARTS
    # =========================================================

    def create_charts(self):

        tasks = load_tasks()

        if not tasks:

            self.create_no_data_card()

            return

        chart_card = self.create_section_card()

        chart_card.pack(
            fill="x",
            padx=10,
            pady=12,
        )

        self.create_section_header(
            chart_card,
            "Study Analytics Charts",
            "Visual breakdown of tasks, priorities and subject progress.",
            "📊",
        )

        chart_frame = ctk.CTkFrame(
            chart_card,
            fg_color="transparent",
        )

        chart_frame.pack(
            fill="x",
            padx=15,
            pady=(6, 15),
        )

        chart_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        chart_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # THEME SETTINGS FOR MATPLOTLIB
        # -----------------------------------------------------

        is_dark = (
            ctk.get_appearance_mode()
            == "Dark"
        )

        if is_dark:

            figure_face = "#181F28"
            axes_face = "#181F28"
            text_color = "#D8E0EA"
            grid_color = "#2A3441"
            edge_color = "#252E39"

        else:

            figure_face = "#FFFFFF"
            axes_face = "#FFFFFF"
            text_color = "#263241"
            grid_color = "#E5E7EB"
            edge_color = "#E3E7ED"

        # -----------------------------------------------------
        # CHART 1: STATUS
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
                if (
                    get_due_status(task)
                    == "Overdue"
                    and not task.get("completed")
                )
            ),
        }

        figure1 = plt.Figure(
            figsize=(5.4, 3.25),
            dpi=90,
            facecolor=figure_face,
        )

        ax1 = figure1.add_subplot(111)

        ax1.set_facecolor(
            axes_face
        )

        bars1 = ax1.bar(
            list(status_counts.keys()),
            list(status_counts.values()),
        )

        ax1.set_title(
            "Task Status",
            color=text_color,
            fontsize=13,
            fontweight="bold",
            pad=12,
        )

        ax1.set_ylabel(
            "Tasks",
            color=text_color,
        )

        ax1.tick_params(
            axis="x",
            colors=text_color,
            rotation=10,
        )

        ax1.tick_params(
            axis="y",
            colors=text_color,
        )

        ax1.grid(
            axis="y",
            color=grid_color,
            alpha=0.7,
            linewidth=0.8,
        )

        ax1.set_axisbelow(
            True
        )

        for spine in ax1.spines.values():

            spine.set_color(
                edge_color
            )

        for bar in bars1:

            height = bar.get_height()

            ax1.text(
                bar.get_x()
                + bar.get_width() / 2,
                height
                + 0.05,
                str(int(height)),
                ha="center",
                va="bottom",
                color=text_color,
                fontsize=10,
                fontweight="bold",
            )

        figure1.tight_layout()

        canvas1 = FigureCanvasTkAgg(
            figure1,
            master=chart_frame,
        )

        canvas1.draw()

        canvas1.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
        )

        # -----------------------------------------------------
        # CHART 2: PRIORITY
        # -----------------------------------------------------

        priority_counts = Counter(
            task.get(
                "priority",
                "Medium",
            )
            for task in tasks
        )

        figure2 = plt.Figure(
            figsize=(5.4, 3.25),
            dpi=90,
            facecolor=figure_face,
        )

        ax2 = figure2.add_subplot(111)

        ax2.set_facecolor(
            axes_face
        )

        labels = list(
            priority_counts.keys()
        )

        values = list(
            priority_counts.values()
        )

        ax2.pie(
            values,
            labels=labels,
            autopct="%1.0f%%",
            textprops={
                "color": text_color,
                "fontsize": 10,
            },
            wedgeprops={
                "linewidth": 1.5,
                "edgecolor": edge_color,
            },
        )

        ax2.set_title(
            "Priority Distribution",
            color=text_color,
            fontsize=13,
            fontweight="bold",
            pad=12,
        )

        figure2.tight_layout()

        canvas2 = FigureCanvasTkAgg(
            figure2,
            master=chart_frame,
        )

        canvas2.draw()

        canvas2.get_tk_widget().grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
        )

        # -----------------------------------------------------
        # CHART 3: SUBJECT PROGRESS
        # -----------------------------------------------------

        subject_data = get_subject_progress()

        if subject_data:

            subjects = list(
                subject_data.keys()
            )

            progress = [
                subject_data[
                    subject
                ]["progress"]
                for subject in subjects
            ]

            figure3 = plt.Figure(
                figsize=(10.8, 3.7),
                dpi=90,
                facecolor=figure_face,
            )

            ax3 = figure3.add_subplot(111)

            ax3.set_facecolor(
                axes_face
            )

            bars3 = ax3.bar(
                subjects,
                progress,
            )

            ax3.set_title(
                "Subject Completion Progress",
                color=text_color,
                fontsize=13,
                fontweight="bold",
                pad=12,
            )

            ax3.set_ylabel(
                "Progress (%)",
                color=text_color,
            )

            ax3.set_ylim(
                0,
                100,
            )

            ax3.tick_params(
                axis="x",
                colors=text_color,
                rotation=25,
            )

            ax3.tick_params(
                axis="y",
                colors=text_color,
            )

            ax3.grid(
                axis="y",
                color=grid_color,
                alpha=0.7,
                linewidth=0.8,
            )

            ax3.set_axisbelow(
                True
            )

            for spine in ax3.spines.values():

                spine.set_color(
                    edge_color
                )

            for bar, value in zip(
                bars3,
                progress,
            ):

                ax3.text(
                    bar.get_x()
                    + bar.get_width() / 2,
                    value + 2,
                    f"{int(value)}%",
                    ha="center",
                    va="bottom",
                    color=text_color,
                    fontsize=9,
                    fontweight="bold",
                )

            figure3.tight_layout()

            canvas3 = FigureCanvasTkAgg(
                figure3,
                master=chart_card,
            )

            canvas3.draw()

            canvas3.get_tk_widget().pack(
                fill="x",
                padx=15,
                pady=(4, 15),
            )

    # =========================================================
    # NO DATA
    # =========================================================

    def create_no_data_card(self):

        card = self.create_section_card()

        card.pack(
            fill="x",
            padx=10,
            pady=12,
        )

        ctk.CTkLabel(
            card,
            text="📊",
            font=("Segoe UI", 38),
            text_color=(
                "#3B82F6",
                "#60A5FA",
            ),
        ).pack(
            pady=(28, 6),
        )

        ctk.CTkLabel(
            card,
            text="Analytics will appear here",
            font=("Segoe UI", 19, "bold"),
        ).pack()

        ctk.CTkLabel(
            card,
            text=(
                "Create a few study tasks to start generating "
                "your performance charts."
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            pady=(5, 28),
        )

    # =========================================================
    # HEATMAP
    # =========================================================

    def create_heatmap(self):

        card = self.create_section_card()

        card.pack(
            fill="x",
            padx=10,
            pady=(0, 12),
        )

        self.create_section_header(
            card,
            "30-Day Study Heatmap",
            "Track recent activity and consistency at a glance.",
            "▦",
        )

        # -----------------------------------------------------
        # DATA
        # -----------------------------------------------------

        tasks = load_tasks()

        study_data = load_study_data()

        study_dates = set(
            study_data.get(
                "study_dates",
                [],
            )
        )

        completion_by_date = {}

        for task in tasks:

            completed_on = task.get(
                "completed_on",
                "",
            )

            if completed_on:

                completion_by_date[
                    completed_on
                ] = (
                    completion_by_date.get(
                        completed_on,
                        0,
                    )
                    + 1
                )

        today = date.today()

        dates = [
            today - timedelta(
                days=offset
            )
            for offset in range(
                29,
                -1,
                -1,
            )
        ]

        # -----------------------------------------------------
        # HEATMAP WRAPPER
        # -----------------------------------------------------

        heatmap_wrapper = ctk.CTkFrame(
            card,
            corner_radius=13,
            fg_color=(
                "#F7F8FA",
                "#151C24",
            ),
        )

        heatmap_wrapper.pack(
            fill="x",
            padx=20,
            pady=(4, 12),
        )

        heatmap = ctk.CTkFrame(
            heatmap_wrapper,
            fg_color="transparent",
        )

        heatmap.pack(
            padx=14,
            pady=14,
        )

        # -----------------------------------------------------
        # DAY LABELS
        # -----------------------------------------------------

        weekday_labels = [
            "M",
            "T",
            "W",
            "T",
            "F",
            "S",
            "S",
        ]

        # Compact 10-column layout.
        for column, label in enumerate(
            weekday_labels
        ):

            ctk.CTkLabel(
                heatmap,
                text=label,
                font=("Segoe UI", 8, "bold"),
                text_color=(
                    "#94A3B8",
                    "#718096",
                ),
            ).grid(
                row=0,
                column=column,
                padx=4,
                pady=(0, 4),
            )

        # -----------------------------------------------------
        # CELLS
        # -----------------------------------------------------

        for index, current_date in enumerate(
            dates
        ):

            row = (
                index // 10
            ) + 1

            column = (
                index % 10
            )

            key = current_date.isoformat()

            completed_count = (
                completion_by_date.get(
                    key,
                    0,
                )
            )

            focus_active = (
                key in study_dates
            )

            if (
                completed_count == 0
                and not focus_active
            ):

                intensity = 0

            elif completed_count <= 1:

                intensity = 1

            elif completed_count <= 3:

                intensity = 2

            else:

                intensity = 3

            # -------------------------------------------------
            # INTENSITY
            # -------------------------------------------------

            if intensity == 0:

                bg = (
                    "#E9EEF3",
                    "#232D38",
                )

                number = (
                    "#64748B",
                    "#7C8A99",
                )

            elif intensity == 1:

                bg = (
                    "#D7E8FF",
                    "#23476D",
                )

                number = (
                    "#2563EB",
                    "#93C5FD",
                )

            elif intensity == 2:

                bg = (
                    "#A9CCFF",
                    "#28619D",
                )

                number = (
                    "#1D4ED8",
                    "#DBEAFE",
                )

            else:

                bg = (
                    "#5E9FF0",
                    "#3478BA",
                )

                number = (
                    "#FFFFFF",
                    "#FFFFFF",
                )

            # Today's cell gets an additional border.
            border_color = (
                "#2563EB"
                if current_date == today
                else (
                    "#D6DEE8",
                    "#2E3946",
                )
            )

            square = ctk.CTkFrame(
                heatmap,
                width=54,
                height=48,
                corner_radius=9,
                fg_color=bg,
                border_width=1
                if current_date == today
                else 0,
                border_color=border_color,
            )

            square.grid(
                row=row,
                column=column,
                padx=3,
                pady=3,
            )

            square.grid_propagate(
                False
            )

            ctk.CTkLabel(
                square,
                text=current_date.strftime(
                    "%d"
                ),
                font=("Segoe UI", 9, "bold"),
                text_color=number,
            ).pack(
                pady=(5, 0),
            )

            count_text = (
                str(completed_count)
                if completed_count
                else "·"
            )

            ctk.CTkLabel(
                square,
                text=count_text,
                font=("Segoe UI", 8),
                text_color=number,
            ).pack()

        # -----------------------------------------------------
        # LEGEND
        # -----------------------------------------------------

        legend = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        legend.pack(
            fill="x",
            padx=20,
            pady=(0, 12),
        )

        ctk.CTkLabel(
            legend,
            text="Less",
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
        )

        for fg in [
            (
                "#E9EEF3",
                "#232D38",
            ),
            (
                "#D7E8FF",
                "#23476D",
            ),
            (
                "#A9CCFF",
                "#28619D",
            ),
            (
                "#5E9FF0",
                "#3478BA",
            ),
        ]:

            box = ctk.CTkFrame(
                legend,
                width=12,
                height=12,
                corner_radius=3,
                fg_color=fg,
            )

            box.pack(
                side="left",
                padx=3,
            )

            box.pack_propagate(
                False
            )

        ctk.CTkLabel(
            legend,
            text="More",
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
            padx=(4, 0),
        )

        ctk.CTkLabel(
            card,
            text=(
                "Activity is based on completed tasks "
                "and recorded focus sessions."
            ),
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 16),
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