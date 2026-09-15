import customtkinter as ctk

from tkinter import filedialog, messagebox

from datetime import datetime

from core.task_manager import (
    load_tasks,
    get_statistics,
    get_streak,
    get_subject_progress,
    load_study_data,
)

from core.gamification import (
    get_gamification_summary,
    get_achievements,
)


class ReportsView(ctk.CTkFrame):

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
        self.create_report()

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
            text="ACADEMIC SUMMARY",
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
            text="Study Report",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            heading,
            text=(
                "A complete overview of your academic progress "
                "and study activity."
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
        # ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        actions.grid(
            row=0,
            column=1,
            padx=(15, 0),
        )

        ctk.CTkButton(
            actions,
            text="↓  Export Report",
            width=145,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            command=self.export_report,
        ).pack(
            side="left",
            padx=4,
        )

        ctk.CTkButton(
            actions,
            text="↻  Refresh",
            width=105,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            fg_color=(
                "#E8EEF6",
                "#273442",
            ),
            hover_color=(
                "#DCE5F0",
                "#344150",
            ),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
            command=self.refresh,
        ).pack(
            side="left",
            padx=4,
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

        for column in range(5):

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
        subtitle,
        icon,
        accent,
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
            padx=13,
            pady=(0, 12),
        )

    # =========================================================
    # REPORT AREA
    # =========================================================

    def create_report(self):

        outer = ctk.CTkFrame(
            self,
            corner_radius=19,
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

        outer.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20),
        )

        outer.grid_columnconfigure(
            0,
            weight=1,
        )

        outer.grid_rowconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # REPORT HEADER
        # -----------------------------------------------------

        report_header = ctk.CTkFrame(
            outer,
            fg_color="transparent",
        )

        report_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(16, 7),
        )

        report_header.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            report_header,
            text="GENERATED REPORT",
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

        self.report_status = ctk.CTkLabel(
            report_header,
            text="Ready",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                "#15803D",
                "#4ADE80",
            ),
        )

        self.report_status.grid(
            row=0,
            column=1,
            sticky="e",
        )

        # -----------------------------------------------------
        # TEXT REPORT
        # -----------------------------------------------------

        self.report = ctk.CTkTextbox(
            outer,
            corner_radius=13,
            font=("Consolas", 11),
            wrap="none",
            fg_color=(
                "#F8FAFC",
                "#121920",
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        self.report.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15),
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        # -----------------------------------------------------
        # CLEAR SUMMARY
        # -----------------------------------------------------

        for widget in self.summary.winfo_children():

            widget.destroy()

        # -----------------------------------------------------
        # CLEAR REPORT
        # -----------------------------------------------------

        self.report.delete(
            "1.0",
            "end",
        )

        tasks = load_tasks()

        stats = get_statistics(
            tasks
        )

        study_data = load_study_data()

        gamification = (
            get_gamification_summary()
        )

        streak = get_streak()

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        self.create_summary_card(
            0,
            "TOTAL TASKS",
            stats["total"],
            "All planned work",
            "📚",
            "#3B82F6",
        )

        self.create_summary_card(
            1,
            "COMPLETED",
            stats["completed"],
            "Finished tasks",
            "✓",
            "#22C55E",
        )

        self.create_summary_card(
            2,
            "COMPLETION",
            f"{stats['progress']}%",
            "Overall progress",
            "↗",
            "#8B5CF6",
        )

        self.create_summary_card(
            3,
            "FOCUS TIME",
            f"{study_data.get('total_focus_minutes', 0)} min",
            "Recorded focus",
            "🧠",
            "#0891B2",
        )

        self.create_summary_card(
            4,
            "LEVEL",
            gamification["level"],
            f"{gamification['xp']} XP earned",
            "⭐",
            "#F59E0B",
        )

        # -----------------------------------------------------
        # BUILD REPORT
        # -----------------------------------------------------

        lines = []

        lines.append(
            "STUDENT STUDY PLANNER"
        )

        lines.append(
            "COMPLETE STUDY REPORT"
        )

        lines.append(
            "=" * 65
        )

        lines.append(
            f"Generated: "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}"
        )

        lines.append("")

        # =====================================================
        # OVERALL PERFORMANCE
        # =====================================================

        lines.append(
            "1. OVERALL PERFORMANCE"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Total tasks              : "
            f"{stats['total']}"
        )

        lines.append(
            f"Completed tasks          : "
            f"{stats['completed']}"
        )

        lines.append(
            f"Pending tasks            : "
            f"{stats['pending']}"
        )

        lines.append(
            f"Tasks due today          : "
            f"{stats['today']}"
        )

        lines.append(
            f"Overdue tasks            : "
            f"{stats['overdue']}"
        )

        lines.append(
            f"Completion rate          : "
            f"{stats['progress']}%"
        )

        lines.append(
            f"Average task progress    : "
            f"{stats['average_progress']}%"
        )

        lines.append("")

        # =====================================================
        # STUDY TIME
        # =====================================================

        lines.append(
            "2. STUDY TIME"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Total planned time       : "
            f"{stats['total_planned_minutes']} minutes"
        )

        lines.append(
            f"Completed study time     : "
            f"{stats['completed_minutes']} minutes"
        )

        lines.append(
            f"Remaining study time     : "
            f"{stats['estimated_minutes']} minutes"
        )

        lines.append(
            f"Total focus time         : "
            f"{study_data.get('total_focus_minutes', 0)} minutes"
        )

        lines.append(
            f"Focus sessions           : "
            f"{gamification['sessions']}"
        )

        lines.append("")

        # =====================================================
        # CONSISTENCY
        # =====================================================

        lines.append(
            "3. STUDY CONSISTENCY"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Current study streak     : "
            f"{streak} days"
        )

        lines.append(
            f"Daily study goal        : "
            f"{study_data.get('daily_goal', 5)} tasks"
        )

        lines.append("")

        # =====================================================
        # SUBJECT PERFORMANCE
        # =====================================================

        lines.append(
            "4. SUBJECT PERFORMANCE"
        )

        lines.append(
            "-" * 35
        )

        subject_data = get_subject_progress()

        if subject_data:

            for subject, data in subject_data.items():

                lines.append(
                    f"{subject:<25} "
                    f"{data['completed']}/{data['total']} "
                    f"completed ({data['progress']}%)"
                )

        else:

            lines.append(
                "No subject data available."
            )

        lines.append("")

        # =====================================================
        # GAMIFICATION
        # =====================================================

        lines.append(
            "5. GAMIFICATION"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Current level            : "
            f"{gamification['level']}"
        )

        lines.append(
            f"Total XP                 : "
            f"{gamification['xp']}"
        )

        lines.append(
            f"XP toward next level     : "
            f"{gamification['progress_xp']} / 500"
        )

        lines.append(
            f"Achievements unlocked    : "
            f"{gamification['achievements']} / "
            f"{gamification['total_achievements']}"
        )

        lines.append("")

        # =====================================================
        # ACHIEVEMENTS
        # =====================================================

        lines.append(
            "6. ACHIEVEMENTS"
        )

        lines.append(
            "-" * 35
        )

        achievements = get_achievements()

        unlocked = [
            achievement
            for achievement in achievements
            if achievement.get(
                "unlocked"
            )
        ]

        if unlocked:

            for achievement in unlocked:

                lines.append(
                    f"{achievement['icon']} "
                    f"{achievement['name']} — "
                    f"{achievement['description']}"
                )

        else:

            lines.append(
                "No achievements unlocked yet."
            )

        lines.append("")

        # =====================================================
        # FINAL MESSAGE
        # =====================================================

        lines.append(
            "=" * 65
        )

        lines.append(
            "Keep studying consistently and keep improving!"
        )

        # -----------------------------------------------------
        # DISPLAY
        # -----------------------------------------------------

        self.report.insert(
            "1.0",
            "\n".join(
                lines
            ),
        )

        self.report_status.configure(
            text=(
                "● REPORT UPDATED"
            )
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_report(self):

        path = filedialog.asksaveasfilename(
            title="Export Study Report",
            defaultextension=".txt",
            initialfile="study_report.txt",
            filetypes=[
                (
                    "Text File",
                    "*.txt",
                )
            ],
        )

        if not path:

            return

        try:

            content = self.report.get(
                "1.0",
                "end",
            )

            with open(
                path,
                "w",
                encoding="utf-8",
            ) as file:

                file.write(
                    content
                )

            messagebox.showinfo(
                "Report Exported",
                "Your study report was exported successfully.",
            )

        except OSError as error:

            messagebox.showerror(
                "Export Failed",
                f"Could not export the report.\n\n{error}",
            )