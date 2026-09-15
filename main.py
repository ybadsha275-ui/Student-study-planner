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
        self.minsize(1100, 700)

        self.current_page = None
        self.current_page_name = "Dashboard"
        self._reminder_visible = False

        # =====================================================
        # VISUAL THEME
        # =====================================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Premium application colors
        self.colors = {
            "sidebar_dark": "#0D1117",
            "sidebar_light": "#F4F6F8",

            "main_dark": "#11161D",
            "main_light": "#F8F9FB",

            "topbar_dark": "#151B23",
            "topbar_light": "#FFFFFF",

            "card_dark": "#181F28",
            "card_light": "#FFFFFF",

            "border_dark": "#252E39",
            "border_light": "#E3E7ED",

            "accent": "#3B82F6",
            "accent_hover": "#2563EB",

            "text_dark": "#F3F4F6",
            "text_light": "#111827",

            "muted_dark": "#8B95A5",
            "muted_light": "#6B7280",

            "nav_hover_dark": "#1D2632",
            "nav_hover_light": "#E9EEF5",

            "active_dark": "#1E4F8C",
            "active_light": "#DCEBFF",
        }

        # =====================================================
        # ROOT GRID
        # =====================================================

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================================
        # BUILD APPLICATION
        # =====================================================

        self.create_sidebar()
        self.create_main_area()

        # =====================================================
        # REMINDER SYSTEM
        # =====================================================

        self.reminder_manager = ReminderManager(self)

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
            width=250,
            corner_radius=0,
            fg_color=(
                self.colors["sidebar_light"],
                self.colors["sidebar_dark"],
            ),
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.sidebar.grid_propagate(False)

        # -----------------------------------------------------
        # BRAND
        # -----------------------------------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(28, 18),
        )

        # Small brand indicator
        brand_row = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent",
        )

        brand_row.pack(
            anchor="w",
            fill="x",
        )

        ctk.CTkLabel(
            brand_row,
            text="●",
            font=("Segoe UI", 15, "bold"),
            text_color=self.colors["accent"],
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ctk.CTkLabel(
            brand_row,
            text="STUDY",
            font=("Segoe UI", 22, "bold"),
        ).pack(
            side="left",
        )

        ctk.CTkLabel(
            logo_frame,
            text="PLANNER",
            font=("Segoe UI", 22, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            logo_frame,
            text="Your academic command center",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            pady=(5, 0),
        )

        # -----------------------------------------------------
        # DIVIDER
        # -----------------------------------------------------

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 18),
        )

        # -----------------------------------------------------
        # NAVIGATION LABEL
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="WORKSPACE",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8),
        )

        # -----------------------------------------------------
        # NAVIGATION BUTTONS
        # -----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "Dashboard",
            self.show_dashboard,
        )

        self.tasks_button = self.create_nav_button(
            "Tasks",
            self.show_tasks,
        )

        self.planner_button = self.create_nav_button(
            "Smart Planner",
            self.show_planner,
        )

        self.calendar_button = self.create_nav_button(
            "Calendar",
            self.show_calendar,
        )

        self.focus_button = self.create_nav_button(
            "Focus Mode",
            self.show_focus,
        )

        self.analytics_button = self.create_nav_button(
            "Analytics",
            self.show_analytics,
        )

        self.achievements_button = self.create_nav_button(
            "Achievements",
            self.show_achievements,
        )

        self.reports_button = self.create_nav_button(
            "Study Report",
            self.show_reports,
        )

        # -----------------------------------------------------
        # SETTINGS SECTION
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="SYSTEM",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(22, 8),
        )

        self.settings_button = self.create_nav_button(
            "Settings",
            self.show_settings,
        )

        # -----------------------------------------------------
        # SIDEBAR BOTTOM
        # -----------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
        )

        spacer.pack(
            fill="both",
            expand=True,
        )

        status_card = ctk.CTkFrame(
            self.sidebar,
            corner_radius=14,
            fg_color=(
                "#E8F1FE",
                "#162334",
            ),
        )

        status_card.pack(
            fill="x",
            padx=16,
            pady=(0, 10),
        )

        ctk.CTkLabel(
            status_card,
            text="●  READY",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors["accent"],
        ).pack(
            anchor="w",
            padx=14,
            pady=(11, 1),
        )

        ctk.CTkLabel(
            status_card,
            text="Study workspace active",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=14,
            pady=(0, 10),
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Student Study Planner",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 2),
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Desktop Edition  •  v1.0",
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 18),
        )

    # =========================================================
    # NAVIGATION BUTTON
    # =========================================================

    def create_nav_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=f"   {text}",
            command=command,
            height=42,
            corner_radius=10,
            anchor="w",
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
            hover_color=(
                self.colors["nav_hover_light"],
                self.colors["nav_hover_dark"],
            ),
            border_width=0,
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2,
        )

        return button

    # =========================================================
    # ACTIVE NAVIGATION STATE
    # =========================================================

    def set_active_button(self, active_button):

        buttons = [
            self.dashboard_button,
            self.tasks_button,
            self.planner_button,
            self.calendar_button,
            self.focus_button,
            self.analytics_button,
            self.achievements_button,
            self.reports_button,
            self.settings_button,
        ]

        for button in buttons:
            try:
                if button == active_button:
                    button.configure(
                        fg_color=(
                            self.colors["active_light"],
                            self.colors["active_dark"],
                        ),
                        text_color=(
                            self.colors["accent"],
                            "#FFFFFF",
                        ),
                    )
                else:
                    button.configure(
                        fg_color="transparent",
                        text_color=(
                            self.colors["text_light"],
                            self.colors["text_dark"],
                        ),
                    )
            except Exception:
                pass

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=(
                self.colors["main_light"],
                self.colors["main_dark"],
            ),
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1,
        )

        self.main_area.grid_rowconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # TOP BAR
        # -----------------------------------------------------

        self.topbar = ctk.CTkFrame(
            self.main_area,
            height=72,
            corner_radius=0,
            fg_color=(
                self.colors["topbar_light"],
                self.colors["topbar_dark"],
            ),
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.topbar.grid_propagate(False)

        self.topbar.grid_columnconfigure(
            0,
            weight=1,
        )

        # Page heading container
        heading_frame = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent",
        )

        heading_frame.grid(
            row=0,
            column=0,
            sticky="w",
            padx=26,
        )

        self.page_title = ctk.CTkLabel(
            heading_frame,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        )

        self.page_title.pack(
            anchor="w",
        )

        self.page_subtitle = ctk.CTkLabel(
            heading_frame,
            text="Plan smarter. Study consistently. Stay ahead.",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(1, 0),
        )

        # -----------------------------------------------------
        # TOP BAR ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent",
        )

        actions.grid(
            row=0,
            column=1,
            padx=(5, 18),
        )

        self.theme_button = ctk.CTkButton(
            actions,
            text="☾",
            width=40,
            height=38,
            corner_radius=10,
            font=("Segoe UI Symbol", 17),
            command=self.toggle_appearance,
            fg_color=(
                "#E9EEF5",
                "#202936",
            ),
            hover_color=(
                "#DDE5EF",
                "#293443",
            ),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        )

        self.theme_button.pack(
            side="left",
            padx=4,
        )

        self.refresh_button = ctk.CTkButton(
            actions,
            text="↻",
            width=40,
            height=38,
            corner_radius=10,
            font=("Segoe UI Symbol", 18),
            command=self.refresh_current_page,
            fg_color=(
                "#E9EEF5",
                "#202936",
            ),
            hover_color=(
                "#DDE5EF",
                "#293443",
            ),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        )

        self.refresh_button.pack(
            side="left",
            padx=4,
        )

        # -----------------------------------------------------
        # PAGE CONTAINER
        # -----------------------------------------------------

        self.page_container = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent",
        )

        self.page_container.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1,
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1,
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

    def set_page_title(self, title):

        self.page_title.configure(
            text=title,
        )

    def set_page_subtitle(self, subtitle):

        self.page_subtitle.configure(
            text=subtitle,
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_page()

        self.set_page_title("Dashboard")
        self.set_page_subtitle(
            "Overview of your study progress and academic workload."
        )

        self.set_active_button(
            self.dashboard_button
        )

        dashboard_scroll = ctk.CTkScrollableFrame(
            self.page_container,
            fg_color="transparent",
        )

        dashboard_scroll.pack(
            fill="both",
            expand=True,
        )

        dashboard = DashboardView(
            dashboard_scroll,
            self,
        )

        dashboard.pack(
            fill="both",
            expand=True,
        )

        self.current_page = dashboard
        self.current_page_name = "Dashboard"

    # =========================================================
    # TASKS
    # =========================================================

    def show_tasks(self):

        self.clear_page()

        self.set_page_title("My Tasks")
        self.set_page_subtitle(
            "Create, organize and track everything you need to study."
        )

        self.set_active_button(
            self.tasks_button
        )

        tasks = TasksView(
            self.page_container,
            self,
        )

        tasks.pack(
            fill="both",
            expand=True,
        )

        self.current_page = tasks
        self.current_page_name = "Tasks"

    # =========================================================
    # SMART PLANNER
    # =========================================================

    def show_planner(self):

        self.clear_page()

        self.set_page_title("Smart Daily Planner")
        self.set_page_subtitle(
            "Build a focused study order based on deadlines and priorities."
        )

        self.set_active_button(
            self.planner_button
        )

        planner = PlannerView(
            self.page_container,
            self,
        )

        planner.pack(
            fill="both",
            expand=True,
        )

        self.current_page = planner
        self.current_page_name = "Smart Planner"

    # =========================================================
    # CALENDAR
    # =========================================================

    def show_calendar(self):

        self.clear_page()

        self.set_page_title("Study Calendar")
        self.set_page_subtitle(
            "Visualize your deadlines and planned study schedule."
        )

        self.set_active_button(
            self.calendar_button
        )

        calendar_view = CalendarView(
            self.page_container,
            self,
        )

        calendar_view.pack(
            fill="both",
            expand=True,
        )

        self.current_page = calendar_view
        self.current_page_name = "Calendar"

    # =========================================================
    # FOCUS
    # =========================================================

    def show_focus(self):

        self.clear_page()

        self.set_page_title("Focus Mode")
        self.set_page_subtitle(
            "Use structured focus sessions to study without distractions."
        )

        self.set_active_button(
            self.focus_button
        )

        focus = FocusView(
            self.page_container,
            self,
        )

        focus.pack(
            fill="both",
            expand=True,
        )

        self.current_page = focus
        self.current_page_name = "Focus"

    # =========================================================
    # ANALYTICS
    # =========================================================

    def show_analytics(self):

        self.clear_page()

        self.set_page_title("Analytics")
        self.set_page_subtitle(
            "Understand your productivity, workload and study activity."
        )

        self.set_active_button(
            self.analytics_button
        )

        analytics = AnalyticsView(
            self.page_container,
            self,
        )

        analytics.pack(
            fill="both",
            expand=True,
        )

        self.current_page = analytics
        self.current_page_name = "Analytics"

    # =========================================================
    # ACHIEVEMENTS
    # =========================================================

    def show_achievements(self):

        self.clear_page()

        self.set_page_title("Achievements")
        self.set_page_subtitle(
            "Track your XP, levels and milestones as you study."
        )

        self.set_active_button(
            self.achievements_button
        )

        achievements = AchievementsView(
            self.page_container,
            self,
        )

        achievements.pack(
            fill="both",
            expand=True,
        )

        self.current_page = achievements
        self.current_page_name = "Achievements"

    # =========================================================
    # STUDY REPORT
    # =========================================================

    def show_reports(self):

        self.clear_page()

        self.set_page_title("Study Report")
        self.set_page_subtitle(
            "Review your academic performance and study consistency."
        )

        self.set_active_button(
            self.reports_button
        )

        reports = ReportsView(
            self.page_container,
            self,
        )

        reports.pack(
            fill="both",
            expand=True,
        )

        self.current_page = reports
        self.current_page_name = "Study Report"

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self):

        self.clear_page()

        self.set_page_title("Settings")
        self.set_page_subtitle(
            "Manage appearance, reminders and application data."
        )

        self.set_active_button(
            self.settings_button
        )

        frame = ctk.CTkScrollableFrame(
            self.page_container,
            corner_radius=18,
            fg_color=(
                self.colors["card_light"],
                self.colors["card_dark"],
            ),
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25,
        )

        # -----------------------------------------------------
        # SETTINGS TITLE
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame,
            text="Settings",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5),
        )

        ctk.CTkLabel(
            frame,
            text="Customize the application and manage your study data.",
            font=("Segoe UI", 13),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 25),
        )

        # -----------------------------------------------------
        # APPEARANCE
        # -----------------------------------------------------

        appearance_card = self.create_settings_card(
            frame,
            "Appearance",
            "Switch between dark and light mode.",
        )

        ctk.CTkButton(
            appearance_card,
            text="Toggle Light / Dark Mode",
            width=220,
            height=38,
            corner_radius=10,
            command=self.toggle_appearance,
        ).pack(
            anchor="w",
            padx=20,
            pady=15,
        )

        # -----------------------------------------------------
        # REMINDERS
        # -----------------------------------------------------

        reminder_card = self.create_settings_card(
            frame,
            "Reminders",
            "Get deadline notifications while the application is running.",
        )

        reminder_var = ctk.BooleanVar(
            value=self.reminder_manager.enabled,
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
            font=("Segoe UI", 13),
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3),
        )

        ctk.CTkLabel(
            reminder_card,
            text=(
                "Checks for overdue, today's and tomorrow's "
                "deadlines while the application is running."
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            wraplength=800,
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15),
        )

        # -----------------------------------------------------
        # BACKUP
        # -----------------------------------------------------

        backup_card = self.create_settings_card(
            frame,
            "Data Backup",
            "Protect your tasks, study history and achievements.",
        )

        backup_buttons = ctk.CTkFrame(
            backup_card,
            fg_color="transparent",
        )

        backup_buttons.pack(
            anchor="w",
            padx=20,
            pady=15,
        )

        ctk.CTkButton(
            backup_buttons,
            text="Export Backup",
            width=150,
            height=38,
            corner_radius=10,
            command=self.export_backup,
        ).pack(
            side="left",
            padx=(0, 10),
        )

        ctk.CTkButton(
            backup_buttons,
            text="Import Backup",
            width=150,
            height=38,
            corner_radius=10,
            fg_color=(
                "#5B6470",
                "#394452",
            ),
            hover_color=(
                "#4B5563",
                "#465364",
            ),
            command=self.import_backup,
        ).pack(
            side="left",
        )

        # -----------------------------------------------------
        # APP INFORMATION
        # -----------------------------------------------------

        info_card = self.create_settings_card(
            frame,
            "Application",
            "Information about your Student Study Planner desktop app.",
        )

        ctk.CTkLabel(
            info_card,
            text=(
                "Student Study Planner\n"
                "Desktop Edition\n"
                "Built with Python + CustomTkinter\n"
                "Version 1.0"
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            justify="left",
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 18),
        )

        self.current_page = frame
        self.current_page_name = "Settings"

    # =========================================================
    # SETTINGS CARD HELPER
    # =========================================================

    def create_settings_card(
        self,
        parent,
        title,
        description,
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=(
                "#F7F8FA",
                "#1A222C",
            ),
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 18, "bold"),
        ).pack(
            anchor="w",
            padx=20,
            pady=(17, 3),
        )

        ctk.CTkLabel(
            card,
            text=description,
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 2),
        )

        return card

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
                    "*.json",
                )
            ],
            initialfile="study_planner_backup.json",
        )

        if not path:
            return

        try:

            create_backup(path)

            messagebox.showinfo(
                "Backup Created",
                "Your complete study planner backup was created successfully.",
            )

        except Exception as error:

            messagebox.showerror(
                "Backup Failed",
                f"Could not create the backup.\n\n{error}",
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
                    "*.json",
                )
            ],
        )

        if not path:
            return

        confirm = messagebox.askyesno(
            "Replace Existing Data",
            (
                "Importing this backup will replace your current "
                "tasks, study data and achievements.\n\n"
                "Continue?"
            ),
        )

        if not confirm:
            return

        try:

            restore_backup(path)

            messagebox.showinfo(
                "Backup Imported",
                (
                    "Backup restored successfully.\n\n"
                    "The application will now refresh."
                ),
            )

            self.show_dashboard()

        except Exception as error:

            messagebox.showerror(
                "Import Failed",
                f"Could not restore the backup.\n\n{error}",
            )

    # =========================================================
    # REFRESH DASHBOARD
    # =========================================================

    def refresh_dashboard(self):

        if isinstance(
            self.current_page,
            DashboardView,
        ):
            self.show_dashboard()

    # =========================================================
    # REFRESH CURRENT PAGE
    # =========================================================

    def refresh_current_page(self):

        if isinstance(
            self.current_page,
            DashboardView,
        ):

            self.show_dashboard()

        elif isinstance(
            self.current_page,
            TasksView,
        ):

            self.show_tasks()

        elif isinstance(
            self.current_page,
            PlannerView,
        ):

            self.show_planner()

        elif isinstance(
            self.current_page,
            CalendarView,
        ):

            self.show_calendar()

        elif isinstance(
            self.current_page,
            FocusView,
        ):

            self.show_focus()

        elif isinstance(
            self.current_page,
            AnalyticsView,
        ):

            self.show_analytics()

        elif isinstance(
            self.current_page,
            AchievementsView,
        ):

            self.show_achievements()

        elif isinstance(
            self.current_page,
            ReportsView,
        ):

            self.show_reports()

        else:
            self.show_settings()

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
                text="☀",
            )

        else:

            ctk.set_appearance_mode(
                "Dark"
            )

            self.theme_button.configure(
                text="☾",
            )

        # Refresh active button colors after switching theme.
        self.refresh_current_page()

    # =========================================================
    # CLOSE APPLICATION
    # =========================================================

    def on_close(self):

        confirm = messagebox.askyesno(
            "Exit Study Planner",
            "Are you sure you want to close the application?",
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
        app.on_close,
    )

    app.mainloop()