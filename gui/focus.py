import customtkinter as ctk
from datetime import date

from core.task_manager import (
    load_tasks,
    load_study_data,
    save_study_data,
    record_focus_session
)

from core.gamification import (
    load_gamification,
    award_session_xp,
    check_achievements,
    get_level,
    get_achievement_definitions
)


class FocusView(ctk.CTkFrame):

    def __init__(self, master, app):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.app = app

        # =====================================================
        # TIMER SETTINGS
        # =====================================================

        self.work_minutes = 25
        self.break_minutes = 5

        self.mode = "Focus"

        self.remaining_seconds = (
            self.work_minutes * 60
        )

        self.timer_running = False
        self.after_id = None

        # =====================================================
        # LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.create_header()
        self.create_settings()
        self.create_timer()
        self.create_session_info()

        self.refresh_task_dropdown()
        self.refresh_session_info()

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
            pady=(20, 5)
        )

        ctk.CTkLabel(
            header,
            text="Focus Mode",
            font=("Segoe UI", 30, "bold")
        ).pack()

        ctk.CTkLabel(
            header,
            text=(
                "Focus on one task, complete sessions, "
                "and earn XP for consistent study."
            ),
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        ).pack(
            pady=(3, 0)
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def create_settings(self):

        settings = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        settings.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=15
        )

        settings.grid_columnconfigure(
            8,
            weight=1
        )

        # -----------------------------------------------------
        # Focus duration
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="Focus",
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=(15, 5),
            pady=14
        )

        self.work_var = ctk.StringVar(
            value="25"
        )

        ctk.CTkEntry(
            settings,
            textvariable=self.work_var,
            width=70
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        ctk.CTkLabel(
            settings,
            text="min"
        ).grid(
            row=0,
            column=2,
            padx=(0, 15)
        )

        # -----------------------------------------------------
        # Break duration
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="Break",
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=0,
            column=3,
            padx=(10, 5)
        )

        self.break_var = ctk.StringVar(
            value="5"
        )

        ctk.CTkEntry(
            settings,
            textvariable=self.break_var,
            width=70
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        ctk.CTkLabel(
            settings,
            text="min"
        ).grid(
            row=0,
            column=5,
            padx=(0, 15)
        )

        ctk.CTkButton(
            settings,
            text="Apply",
            width=90,
            command=self.apply_settings
        ).grid(
            row=0,
            column=6,
            padx=10
        )

        # -----------------------------------------------------
        # Task selection
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="Study Task",
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=0,
            column=7,
            padx=(20, 5)
        )

        self.task_var = ctk.StringVar(
            value="No task selected"
        )

        self.task_dropdown = ctk.CTkComboBox(
            settings,
            variable=self.task_var,
            values=[
                "No task selected"
            ],
            width=300
        )

        self.task_dropdown.grid(
            row=0,
            column=8,
            padx=(5, 15),
            sticky="ew"
        )

        self.task_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.update_selected_task_label()
        )

    # =========================================================
    # TIMER
    # =========================================================

    def create_timer(self):

        timer_card = ctk.CTkFrame(
            self,
            corner_radius=20
        )

        timer_card.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=10
        )

        timer_card.grid_columnconfigure(
            0,
            weight=1
        )

        timer_card.grid_rowconfigure(
            0,
            weight=1
        )

        inner = ctk.CTkFrame(
            timer_card,
            fg_color="transparent"
        )

        inner.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        ctk.CTkLabel(
            inner,
            text="CURRENT SESSION",
            font=("Segoe UI", 12, "bold"),
            text_color=("gray45", "gray65")
        ).pack(
            pady=(40, 5)
        )

        self.mode_label = ctk.CTkLabel(
            inner,
            text="FOCUS",
            font=("Segoe UI", 17, "bold")
        )

        self.mode_label.pack()

        self.timer_label = ctk.CTkLabel(
            inner,
            text="25:00",
            font=("Segoe UI", 72, "bold")
        )

        self.timer_label.pack(
            pady=15
        )

        self.selected_task_label = ctk.CTkLabel(
            inner,
            text="No task selected",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray65")
        )

        self.selected_task_label.pack(
            pady=(0, 15)
        )

        buttons = ctk.CTkFrame(
            inner,
            fg_color="transparent"
        )

        buttons.pack(
            pady=(0, 30)
        )

        self.start_button = ctk.CTkButton(
            buttons,
            text="Start",
            width=130,
            height=42,
            font=("Segoe UI", 13, "bold"),
            command=self.start_pause
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.reset_button = ctk.CTkButton(
            buttons,
            text="Reset",
            width=130,
            height=42,
            command=self.reset_timer
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

    # =========================================================
    # SESSION INFORMATION
    # =========================================================

    def create_session_info(self):

        self.info_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.info_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 20)
        )

        self.info_label = ctk.CTkLabel(
            self.info_card,
            text="Today's sessions: 0",
            font=("Segoe UI", 14),
            text_color=("gray40", "gray65")
        )

        self.info_label.pack(
            pady=15
        )

    # =========================================================
    # TASK DROPDOWN
    # =========================================================

    def refresh_task_dropdown(self):

        tasks = [
            task
            for task in load_tasks()
            if not task.get("completed")
        ]

        values = [
            "No task selected"
        ]

        for task in tasks:

            values.append(
                f"{task['id']}|"
                f"{task.get('task', 'Untitled Task')}"
            )

        self.task_dropdown.configure(
            values=values
        )

        current = self.task_var.get()

        if current not in values:
            self.task_var.set(
                values[0]
            )

        self.update_selected_task_label()

    def update_selected_task_label(self):

        selected = self.task_var.get()

        if "|" in selected:

            task_name = selected.split(
                "|",
                1
            )[1]

            self.selected_task_label.configure(
                text=f"Selected: {task_name}"
            )

        else:

            self.selected_task_label.configure(
                text="No task selected"
            )

    # =========================================================
    # SETTINGS
    # =========================================================

    def apply_settings(self):

        try:

            work = int(
                self.work_var.get()
            )

            break_time = int(
                self.break_var.get()
            )

            if work <= 0 or break_time <= 0:
                raise ValueError

        except ValueError:

            self.work_var.set("25")
            self.break_var.set("5")

            work = 25
            break_time = 5

        # Don't reset a session currently running.
        if self.timer_running:
            return

        self.work_minutes = work
        self.break_minutes = break_time

        self.mode = "Focus"

        self.remaining_seconds = (
            self.work_minutes * 60
        )

        self.mode_label.configure(
            text="FOCUS"
        )

        self.start_button.configure(
            text="Start"
        )

        self.update_timer_label()

    # =========================================================
    # START / PAUSE
    # =========================================================

    def start_pause(self):

        if self.timer_running:

            self.timer_running = False

            self.start_button.configure(
                text="Resume"
            )

            return

        self.timer_running = True

        self.start_button.configure(
            text="Pause"
        )

        self.run_timer()

    # =========================================================
    # RUN TIMER
    # =========================================================

    def run_timer(self):

        if not self.timer_running:
            return

        self.update_timer_label()

        if self.remaining_seconds <= 0:

            self.timer_finished()

            return

        self.remaining_seconds -= 1

        self.after_id = self.after(
            1000,
            self.run_timer
        )

    # =========================================================
    # TIMER FINISHED
    # =========================================================

    def timer_finished(self):

        self.timer_running = False

        if self.after_id is not None:

            try:
                self.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

            self.after_id = None

        # -----------------------------------------------------
        # FOCUS FINISHED
        # -----------------------------------------------------

        if self.mode == "Focus":

            self.complete_focus_session()

            self.mode = "Break"

            self.remaining_seconds = (
                self.break_minutes * 60
            )

            self.mode_label.configure(
                text="BREAK"
            )

            self.start_button.configure(
                text="Start Break"
            )

        # -----------------------------------------------------
        # BREAK FINISHED
        # -----------------------------------------------------

        else:

            self.mode = "Focus"

            self.remaining_seconds = (
                self.work_minutes * 60
            )

            self.mode_label.configure(
                text="FOCUS"
            )

            self.start_button.configure(
                text="Start Focus"
            )

        self.update_timer_label()

    # =========================================================
    # RESET
    # =========================================================

    def reset_timer(self):

        self.timer_running = False

        if self.after_id is not None:

            try:
                self.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

            self.after_id = None

        self.mode = "Focus"

        self.remaining_seconds = (
            self.work_minutes * 60
        )

        self.mode_label.configure(
            text="FOCUS"
        )

        self.start_button.configure(
            text="Start"
        )

        self.update_timer_label()

    # =========================================================
    # TIMER DISPLAY
    # =========================================================

    def update_timer_label(self):

        minutes = (
            self.remaining_seconds
            // 60
        )

        seconds = (
            self.remaining_seconds
            % 60
        )

        self.timer_label.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

    # =========================================================
    # COMPLETE FOCUS SESSION
    # =========================================================

    def complete_focus_session(self):

        # -----------------------------------------------------
        # 1. Save focus time / study date
        # -----------------------------------------------------

        record_focus_session(
            self.work_minutes
        )

        # -----------------------------------------------------
        # 2. Read XP state before awarding
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # 3. Award XP
        # -----------------------------------------------------

        earned = award_session_xp()

        # -----------------------------------------------------
        # 4. Check updated level
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # 5. Check achievements
        # -----------------------------------------------------

        newly_unlocked = check_achievements()

        # -----------------------------------------------------
        # 6. Refresh information
        # -----------------------------------------------------

        self.refresh_session_info()

        # -----------------------------------------------------
        # 7. Notify user
        # -----------------------------------------------------

        if new_level > old_level:

            self.show_game_notification(
                "🎉 LEVEL UP!",
                (
                    f"You reached Level {new_level}!\n\n"
                    f"+{earned} XP earned."
                )
            )

        elif newly_unlocked:

            names = self.get_achievement_names(
                newly_unlocked
            )

            self.show_game_notification(
                "🏆 Achievement Unlocked!",
                (
                    f"+{earned} XP earned!\n\n"
                    + "\n".join(names)
                )
            )

        else:

            self.show_game_notification(
                "🧠 Focus Session Complete",
                (
                    f"+{earned} XP earned!\n"
                    f"{self.work_minutes} minutes added to your focus time."
                )
            )

        # -----------------------------------------------------
        # 8. Refresh dashboard if it is open
        # -----------------------------------------------------

        if hasattr(
            self.app,
            "refresh_dashboard"
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # ACHIEVEMENT NAMES
    # =========================================================

    def get_achievement_names(
        self,
        achievement_ids
    ):

        definitions = {
            achievement["id"]: achievement
            for achievement in get_achievement_definitions()
        }

        names = []

        for achievement_id in achievement_ids:

            achievement = definitions.get(
                achievement_id
            )

            if achievement:

                names.append(
                    f"{achievement['icon']} "
                    f"{achievement['name']}"
                )

        return names

    # =========================================================
    # GAME NOTIFICATION
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
    # SESSION INFO
    # =========================================================

    def refresh_session_info(self):

        data = load_study_data()

        today = date.today().isoformat()

        sessions = data.get(
            "pomodoro_sessions",
            {}
        )

        count = sessions.get(
            today,
            0
        )

        total_minutes = data.get(
            "total_focus_minutes",
            0
        )

        self.info_label.configure(
            text=(
                f"Today's sessions: {count}"
                f"     •     "
                f"Total focus time: {total_minutes} min"
            )
        )

    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):

        if self.after_id is not None:

            try:
                self.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

            self.after_id = None

        super().destroy()