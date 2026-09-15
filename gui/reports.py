import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime

from core.task_manager import (
    load_tasks,
    get_statistics,
    get_streak,
    get_subject_progress,
    load_study_data
)

from core.gamification import (
    get_gamification_summary,
    get_achievements
)


class ReportsView(ctk.CTkFrame):

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
        self.create_report()

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
            text="Study Report",
            font=("Segoe UI", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="A complete overview of your academic progress and study activity.",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0)
        )

        ctk.CTkButton(
            header,
            text="Export Report",
            width=150,
            command=self.export_report
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10
        )

        ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            command=self.refresh
        ).grid(
            row=0,
            column=2,
            rowspan=2
        )

    # =========================================================
    # SUMMARY
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

        for column in range(5):

            self.summary.grid_columnconfigure(
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
            font=("Segoe UI", 10),
            text_color=("gray45", "gray65")
        ).pack(
            pady=(12, 2)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 21, "bold")
        ).pack(
            pady=(0, 12)
        )

    # =========================================================
    # REPORT AREA
    # =========================================================

    def create_report(self):

        self.report = ctk.CTkTextbox(
            self,
            corner_radius=15,
            font=("Consolas", 12)
        )

        self.report.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 20)
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        # Clear summary cards
        for widget in self.summary.winfo_children():
            widget.destroy()

        # Clear report
        self.report.delete(
            "1.0",
            "end"
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
        # Summary
        # -----------------------------------------------------

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
            "Completion",
            f"{stats['progress']}%"
        )

        self.create_summary_card(
            3,
            "Focus Time",
            f"{study_data.get('total_focus_minutes', 0)} min"
        )

        self.create_summary_card(
            4,
            "Level",
            gamification["level"]
        )

        # -----------------------------------------------------
        # Build report
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
            f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
        )

        lines.append("")

        # -----------------------------------------------------
        # Overall
        # -----------------------------------------------------

        lines.append(
            "1. OVERALL PERFORMANCE"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Total tasks              : {stats['total']}"
        )

        lines.append(
            f"Completed tasks          : {stats['completed']}"
        )

        lines.append(
            f"Pending tasks            : {stats['pending']}"
        )

        lines.append(
            f"Tasks due today         : {stats['today']}"
        )

        lines.append(
            f"Overdue tasks            : {stats['overdue']}"
        )

        lines.append(
            f"Completion rate          : {stats['progress']}%"
        )

        lines.append(
            f"Average task progress    : {stats['average_progress']}%"
        )

        lines.append("")

        # -----------------------------------------------------
        # Study time
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Consistency
        # -----------------------------------------------------

        lines.append(
            "3. STUDY CONSISTENCY"
        )

        lines.append(
            "-" * 35
        )

        lines.append(
            f"Current study streak     : {streak} days"
        )

        lines.append(
            f"Daily study goal        : "
            f"{study_data.get('daily_goal', 5)} tasks"
        )

        lines.append("")

        # -----------------------------------------------------
        # Subjects
        # -----------------------------------------------------

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
                    f"{data['completed']}/{data['total']} completed "
                    f"({data['progress']}%)"
                )

        else:

            lines.append(
                "No subject data available."
            )

        lines.append("")

        # -----------------------------------------------------
        # Gamification
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Achievements
        # -----------------------------------------------------

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
            if achievement.get("unlocked")
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

        lines.append(
            "=" * 65
        )

        lines.append(
            "Keep studying consistently and keep improving!"
        )

        # -----------------------------------------------------
        # Display
        # -----------------------------------------------------

        self.report.insert(
            "1.0",
            "\n".join(lines)
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
                    "*.txt"
                )
            ]
        )

        if not path:
            return

        try:

            content = self.report.get(
                "1.0",
                "end"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    content
                )

            messagebox.showinfo(
                "Report Exported",
                "Your study report was exported successfully."
            )

        except OSError as error:

            messagebox.showerror(
                "Export Failed",
                f"Could not export the report.\n\n{error}"
            )