import logging
from tkinter import TclError, filedialog, messagebox

import customtkinter as ctk

from core.backup_manager import (
    create_backup,
    restore_backup,
)
from gui.achievements import AchievementsView
from gui.analytics import AnalyticsView
from gui.calendar import CalendarView
from gui.dashboard import DashboardView
from gui.focus import FocusView
from gui.planner import PlannerView
from gui.reminders import ReminderManager
from gui.reports import ReportsView
from gui.tasks import TasksView


class StudyPlannerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================================
        # APPLICATION SETTINGS
        # =====================================================

        self.title("Student Study Planner")

        self.geometry("1400x850")

        self.minsize(
            1100,
            700
        )

        self.current_page = None
        self._reminder_visible = False

        # =====================================================
        # THEME
        # =====================================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # =====================================================
        # ROOT GRID
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # =====================================================
        # BUILD APPLICATION
        # =====================================================

        self.create_sidebar()
        self.create_main_area()

        # =====================================================
        # REMINDER SYSTEM
        # =====================================================

        self.reminder_manager = ReminderManager(
            self
        )

        # =====================================================
        # START PAGE
        # =====================================================

        self.show_dashboard()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # -----------------------------------------------------
        # BRAND
        # -----------------------------------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=18,
            pady=(25, 20)
        )

        ctk.CTkLabel(
            logo_frame,
            text="STUDY",
            font=("Segoe UI", 24, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            logo_frame,
            text="PLANNER",
            font=("Segoe UI", 24, "bold"),
            text_color=("gray45", "gray65")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            logo_frame,
            text="Your academic command center",
            font=("Segoe UI", 10),
            text_color=("gray50", "gray65")
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # NAVIGATION LABEL
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=("Segoe UI", 10, "bold"),
            text_color=("gray45", "gray65")
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 8)
        )

        # -----------------------------------------------------
        # NAVIGATION BUTTONS
        # -----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "Dashboard",
            self.show_dashboard
        )

        self.tasks_button = self.create_nav_button(
            "Tasks",
            self.show_tasks
        )

        self.planner_button = self.create_nav_button(
            "Smart Planner",
            self.show_planner
        )

        self.calendar_button = self.create_nav_button(
            "Calendar",
            self.show_calendar
        )

        self.focus_button = self.create_nav_button(
            "Focus",
            self.show_focus
        )

        self.analytics_button = self.create_nav_button(
            "Analytics",
            self.show_analytics
        )

        self.achievements_button = self.create_nav_button(
            "Achievements",
            self.show_achievements
        )

        self.reports_button = self.create_nav_button(
            "Study Report",
            self.show_reports
        )

        self.settings_button = self.create_nav_button(
            "Settings",
            self.show_settings
        )

        # -----------------------------------------------------
        # SIDEBAR BOTTOM
        # -----------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Student Study Planner",
            font=("Segoe UI", 10, "bold"),
            text_color=("gray45", "gray60")
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 2)
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Desktop Edition",
            font=("Segoe UI", 9),
            text_color=("gray50", "gray65")
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

    def create_nav_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            height=40,
            corner_radius=10,
            anchor="w",
            font=("Segoe UI", 13),
            fg_color="transparent",
            hover_color=("gray78", "gray22")
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2
        )

        return button

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=("gray95", "#111111")
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_area.grid_rowconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # TOP BAR
        # -----------------------------------------------------

        self.topbar = ctk.CTkFrame(
            self.main_area,
            height=65,
            corner_radius=0,
            fg_color=("gray92", "#171717")
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.topbar.grid_propagate(False)

        self.topbar.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_title = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 19, "bold")
        )

        self.page_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25
        )

        # Theme button

        self.theme_button = ctk.CTkButton(
            self.topbar,
            text="☾",
            width=42,
            height=35,
            command=self.toggle_appearance
        )

        self.theme_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # Refresh button

        self.refresh_button = ctk.CTkButton(
            self.topbar,
            text="↻",
            width=42,
            height=35,
            command=self.refresh_current_page
        )

        self.refresh_button.grid(
            row=0,
            column=2,
            padx=(0, 15)
        )

        # -----------------------------------------------------
        # PAGE CONTAINER
        # -----------------------------------------------------

        self.page_container = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.page_container.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1
        )

    # =========================================================
    # PAGE MANAGEMENT
    # =========================================================

    def clear_page(self):

        for widget in self.page_container.winfo_children():

            try:
                widget.destroy()
            except Exception:
                pass

        self.current_page = None

    def set_page_title(
        self,
        title
    ):

        self.page_title.configure(
            text=title
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_page()

        self.set_page_title(
            "Dashboard"
        )

        dashboard_scroll = ctk.CTkScrollableFrame(
            self.page_container,
            fg_color="transparent"
        )

        dashboard_scroll.pack(
            fill="both",
            expand=True
        )

        dashboard = DashboardView(
            dashboard_scroll,
            self
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

        self.current_page = dashboard

    # =========================================================
    # TASKS
    # =========================================================

    def show_tasks(self):

        self.clear_page()

        self.set_page_title(
            "My Tasks"
        )

        tasks = TasksView(
            self.page_container,
            self
        )

        tasks.pack(
            fill="both",
            expand=True
        )

        self.current_page = tasks

    # =========================================================
    # SMART PLANNER
    # =========================================================

    def show_planner(self):

        self.clear_page()

        self.set_page_title(
            "Smart Daily Planner"
        )

        planner = PlannerView(
            self.page_container,
            self
        )

        planner.pack(
            fill="both",
            expand=True
        )

        self.current_page = planner

    # =========================================================
    # CALENDAR
    # =========================================================

    def show_calendar(self):

        self.clear_page()

        self.set_page_title(
            "Study Calendar"
        )

        calendar_view = CalendarView(
            self.page_container,
            self
        )

        calendar_view.pack(
            fill="both",
            expand=True
        )

        self.current_page = calendar_view

    # =========================================================
    # FOCUS
    # =========================================================

    def show_focus(self):

        self.clear_page()

        self.set_page_title(
            "Focus Mode"
        )

        focus = FocusView(
            self.page_container,
            self
        )

        focus.pack(
            fill="both",
            expand=True
        )

        self.current_page = focus

    # =========================================================
    # ANALYTICS
    # =========================================================

    def show_analytics(self):

        self.clear_page()

        self.set_page_title(
            "Analytics"
        )

        analytics = AnalyticsView(
            self.page_container,
            self
        )

        analytics.pack(
            fill="both",
            expand=True
        )

        self.current_page = analytics

    # =========================================================
    # ACHIEVEMENTS
    # =========================================================

    def show_achievements(self):

        self.clear_page()

        self.set_page_title(
            "Achievements"
        )

        achievements = AchievementsView(
            self.page_container,
            self
        )

        achievements.pack(
            fill="both",
            expand=True
        )

        self.current_page = achievements

    # =========================================================
    # STUDY REPORT
    # =========================================================

    def show_reports(self):

        self.clear_page()

        self.set_page_title(
            "Study Report"
        )

        reports = ReportsView(
            self.page_container,
            self
        )

        reports.pack(
            fill="both",
            expand=True
        )

        self.current_page = reports

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self):

        self.clear_page()

        self.set_page_title(
            "Settings"
        )

        frame = ctk.CTkScrollableFrame(
            self.page_container,
            corner_radius=18
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # -----------------------------------------------------
        # SETTINGS TITLE
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame,
            text="Settings",
            font=("Segoe UI", 30, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            frame,
            text="Control appearance, reminders and your data.",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 25)
        )

        # -----------------------------------------------------
        # APPEARANCE
        # -----------------------------------------------------

        appearance_card = ctk.CTkFrame(
            frame,
            corner_radius=15
        )

        appearance_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            appearance_card,
            text="Appearance",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            appearance_card,
            text="Switch between dark and light mode.",
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65")
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkButton(
            appearance_card,
            text="Toggle Light / Dark Mode",
            width=220,
            command=self.toggle_appearance
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # -----------------------------------------------------
        # REMINDERS
        # -----------------------------------------------------

        reminder_card = ctk.CTkFrame(
            frame,
            corner_radius=15
        )

        reminder_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            reminder_card,
            text="Reminders",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        reminder_var = ctk.BooleanVar(
            value=self.reminder_manager.enabled
        )

        def change_reminders():

            self.reminder_manager.set_enabled(
                reminder_var.get()
            )

        ctk.CTkCheckBox(
            reminder_card,
            text="Enable study deadline reminders",
            variable=reminder_var,
            command=change_reminders,
            font=("Segoe UI", 13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        ctk.CTkLabel(
            reminder_card,
            text=(
                "Checks for overdue, today's and tomorrow's "
                "deadlines while the application is running."
            ),
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65"),
            wraplength=800
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # BACKUP
        # -----------------------------------------------------

        backup_card = ctk.CTkFrame(
            frame,
            corner_radius=15
        )

        backup_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            backup_card,
            text="Data Backup",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            backup_card,
            text=(
                "Export your tasks, study data and achievements "
                "into one backup file."
            ),
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65"),
            wraplength=800
        ).pack(
            anchor="w",
            padx=20
        )

        backup_buttons = ctk.CTkFrame(
            backup_card,
            fg_color="transparent"
        )

        backup_buttons.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        ctk.CTkButton(
            backup_buttons,
            text="Export Backup",
            width=150,
            command=self.export_backup
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            backup_buttons,
            text="Import Backup",
            width=150,
            command=self.import_backup
        ).pack(
            side="left"
        )

        # -----------------------------------------------------
        # APP INFORMATION
        # -----------------------------------------------------

        info_card = ctk.CTkFrame(
            frame,
            corner_radius=15
        )

        info_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            info_card,
            text="Application",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            info_card,
            text=(
                "Student Study Planner\n"
                "Desktop Edition\n"
                "Built with Python + CustomTkinter"
            ),
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65"),
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.current_page = frame

    # =========================================================
    # EXPORT BACKUP
    # =========================================================

    def export_backup(self):

        path = filedialog.asksaveasfilename(
            title="Export Study Planner Backup",
            defaultextension=".json",
            filetypes=[
                (
                    "JSON Backup",
                    "*.json"
                )
            ],
            initialfile="study_planner_backup.json"
        )

        if not path:
            return

        try:

            create_backup(
                path
            )

            messagebox.showinfo(
                "Backup Created",
                "Your complete study planner backup was created successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Backup Failed",
                f"Could not create the backup.\n\n{error}"
            )

    # =========================================================
    # IMPORT BACKUP
    # =========================================================

    def import_backup(self):

        path = filedialog.askopenfilename(
            title="Import Study Planner Backup",
            filetypes=[
                (
                    "JSON Backup",
                    "*.json"
                )
            ]
        )

        if not path:
            return

        confirm = messagebox.askyesno(
            "Replace Existing Data",
            (
                "Importing this backup will replace your current "
                "tasks, study data and achievements.\n\n"
                "Continue?"
            )
        )

        if not confirm:
            return

        try:

            restore_backup(
                path
            )

            messagebox.showinfo(
                "Backup Imported",
                (
                    "Backup restored successfully.\n\n"
                    "The application will now refresh."
                )
            )

            self.show_dashboard()

        except Exception as error:

            messagebox.showerror(
                "Import Failed",
                f"Could not restore the backup.\n\n{error}"
            )

    # =========================================================
    # REFRESH DASHBOARD
    # =========================================================

    def refresh_dashboard(self):

        if isinstance(
            self.current_page,
            DashboardView
        ):
            self.show_dashboard()

    # =========================================================
    # REFRESH CURRENT PAGE
    # =========================================================

    def refresh_current_page(self):

        if isinstance(
            self.current_page,
            DashboardView
        ):

            self.show_dashboard()

        elif isinstance(
            self.current_page,
            TasksView
        ):

            self.show_tasks()

        elif isinstance(
            self.current_page,
            PlannerView
        ):

            self.show_planner()

        elif isinstance(
            self.current_page,
            CalendarView
        ):

            self.show_calendar()

        elif isinstance(
            self.current_page,
            FocusView
        ):

            self.show_focus()

        elif isinstance(
            self.current_page,
            AnalyticsView
        ):

            self.show_analytics()

        elif isinstance(
            self.current_page,
            AchievementsView
        ):

            self.show_achievements()

        elif isinstance(
            self.current_page,
            ReportsView
        ):

            self.show_reports()

    # =========================================================
    # APPEARANCE
    # =========================================================

    def toggle_appearance(self):

        current = ctk.get_appearance_mode()

        if current == "Dark":

            ctk.set_appearance_mode(
                "Light"
            )

            self.theme_button.configure(
                text="☀"
            )

        else:

            ctk.set_appearance_mode(
                "Dark"
            )

            self.theme_button.configure(
                text="☾"
            )

    # =========================================================
    # CLOSE APPLICATION
    # =========================================================

    def on_close(self):

        confirm = messagebox.askyesno(
            "Exit Study Planner",
            "Are you sure you want to close the application?"
        )

        if not confirm:
            return

        try:

            self.reminder_manager.stop()

        except Exception:
            pass

        self.destroy()


# =============================================================
# APPLICATION START
# =============================================================

if __name__ == "__main__":

    app = StudyPlannerApp()

    app.protocol(
        "WM_DELETE_WINDOW",
        app.on_close
    )

    app.mainloop()