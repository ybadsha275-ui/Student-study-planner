import customtkinter as ctk

from datetime import date

from core.task_manager import (
    load_tasks,
    load_study_data,
    record_focus_session,
)

from core.gamification import (
    load_gamification,
    award_session_xp,
    check_achievements,
    get_level,
    get_achievement_definitions,
)


class FocusView(ctk.CTkFrame):

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
            weight=1,
        )

        self.grid_rowconfigure(
            2,
            weight=1,
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
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10),
        )

        ctk.CTkLabel(
            header,
            text="FOCUS WORKSPACE",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            header,
            text="Focus Mode",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            header,
            text=(
                "Work deeply, take intentional breaks, "
                "and build consistent study momentum."
            ),
            font=("Segoe UI", 12),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def create_settings(self):

        settings = ctk.CTkFrame(
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

        settings.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        settings.grid_columnconfigure(
            8,
            weight=1,
        )

        # -----------------------------------------------------
        # FOCUS
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="FOCUS",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=0,
            padx=(17, 5),
            pady=(12, 0),
        )

        self.work_var = ctk.StringVar(
            value="25",
        )

        ctk.CTkEntry(
            settings,
            textvariable=self.work_var,
            width=68,
            height=34,
            corner_radius=9,
            justify="center",
        ).grid(
            row=1,
            column=0,
            padx=(15, 4),
            pady=(2, 12),
        )

        ctk.CTkLabel(
            settings,
            text="min",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(2, 12),
        )

        # -----------------------------------------------------
        # BREAK
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="BREAK",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=2,
            padx=(8, 5),
            pady=(12, 0),
        )

        self.break_var = ctk.StringVar(
            value="5",
        )

        ctk.CTkEntry(
            settings,
            textvariable=self.break_var,
            width=68,
            height=34,
            corner_radius=9,
            justify="center",
        ).grid(
            row=1,
            column=2,
            padx=(8, 4),
            pady=(2, 12),
        )

        ctk.CTkLabel(
            settings,
            text="min",
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=1,
            column=3,
            padx=(0, 10),
            pady=(2, 12),
        )

        # -----------------------------------------------------
        # APPLY
        # -----------------------------------------------------

        ctk.CTkButton(
            settings,
            text="Apply",
            width=82,
            height=34,
            corner_radius=9,
            font=("Segoe UI", 10, "bold"),
            command=self.apply_settings,
        ).grid(
            row=1,
            column=4,
            padx=6,
            pady=(2, 12),
        )

        # -----------------------------------------------------
        # TASK LABEL
        # -----------------------------------------------------

        ctk.CTkLabel(
            settings,
            text="STUDY TASK",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=6,
            padx=(25, 6),
            pady=(12, 0),
        )

        # -----------------------------------------------------
        # TASK DROPDOWN
        # -----------------------------------------------------

        self.task_var = ctk.StringVar(
            value="No task selected",
        )

        self.task_dropdown = ctk.CTkComboBox(
            settings,
            variable=self.task_var,
            values=[
                "No task selected",
            ],
            width=310,
            height=34,
            corner_radius=9,
        )

        self.task_dropdown.grid(
            row=1,
            column=6,
            columnspan=3,
            padx=(20, 15),
            pady=(2, 12),
            sticky="ew",
        )

        self.task_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.update_selected_task_label(),
        )

    # =========================================================
    # TIMER
    # =========================================================

    def create_timer(self):

        timer_card = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color=(
                "#F5F8FC",
                "#121A23",
            ),
            border_width=1,
            border_color=(
                "#DDE6F2",
                "#253241",
            ),
        )

        timer_card.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 14),
        )

        timer_card.grid_columnconfigure(
            0,
            weight=1,
        )

        timer_card.grid_rowconfigure(
            0,
            weight=1,
        )

        inner = ctk.CTkFrame(
            timer_card,
            fg_color="transparent",
        )

        inner.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=30,
            pady=25,
        )

        inner.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # SESSION LABEL
        # -----------------------------------------------------

        ctk.CTkLabel(
            inner,
            text="CURRENT SESSION",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            pady=(18, 7),
        )

        # -----------------------------------------------------
        # MODE BADGE
        # -----------------------------------------------------

        self.mode_badge = ctk.CTkFrame(
            inner,
            width=128,
            height=34,
            corner_radius=17,
            fg_color=(
                "#DBEAFE",
                "#173252",
            ),
        )

        self.mode_badge.pack()

        self.mode_badge.pack_propagate(False)

        self.mode_label = ctk.CTkLabel(
            self.mode_badge,
            text="●  FOCUS",
            font=("Segoe UI", 11, "bold"),
            text_color=(
                "#2563EB",
                "#60A5FA",
            ),
        )

        self.mode_label.pack(
            expand=True,
        )

        # -----------------------------------------------------
        # TIMER
        # -----------------------------------------------------

        self.timer_label = ctk.CTkLabel(
            inner,
            text="25:00",
            font=("Segoe UI", 82, "bold"),
            text_color=(
                "#111827",
                "#F8FAFC",
            ),
        )

        self.timer_label.pack(
            pady=(12, 2),
        )

        # -----------------------------------------------------
        # SELECTED TASK
        # -----------------------------------------------------

        self.selected_task_label = ctk.CTkLabel(
            inner,
            text="No task selected",
            font=("Segoe UI", 13, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        )

        self.selected_task_label.pack(
            pady=(0, 16),
        )

        # -----------------------------------------------------
        # TIMER PROGRESS
        # -----------------------------------------------------

        self.timer_progress = ctk.CTkProgressBar(
            inner,
            height=6,
            corner_radius=3,
            progress_color=(
                "#3B82F6",
                "#3B82F6",
            ),
            fg_color=(
                "#DCE4EE",
                "#273241",
            ),
        )

        self.timer_progress.pack(
            fill="x",
            padx=110,
            pady=(0, 20),
        )

        self.timer_progress.set(0)

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        buttons = ctk.CTkFrame(
            inner,
            fg_color="transparent",
        )

        buttons.pack(
            pady=(0, 10),
        )

        self.start_button = ctk.CTkButton(
            buttons,
            text="▶  Start Focus",
            width=150,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 12, "bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.start_pause,
        )

        self.start_button.pack(
            side="left",
            padx=5,
        )

        self.reset_button = ctk.CTkButton(
            buttons,
            text="↻  Reset",
            width=120,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 12, "bold"),
            fg_color=(
                "#E6EBF2",
                "#293542",
            ),
            hover_color=(
                "#D9E1EA",
                "#344353",
            ),
            text_color=(
                "#334155",
                "#E2E8F0",
            ),
            command=self.reset_timer,
        )

        self.reset_button.pack(
            side="left",
            padx=5,
        )

    # =========================================================
    # SESSION INFORMATION
    # =========================================================

    def create_session_info(self):

        self.info_card = ctk.CTkFrame(
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

        self.info_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 20),
        )

        info_inner = ctk.CTkFrame(
            self.info_card,
            fg_color="transparent",
        )

        info_inner.pack(
            pady=14,
        )

        ctk.CTkLabel(
            info_inner,
            text="TODAY",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        self.info_label = ctk.CTkLabel(
            info_inner,
            text="0 sessions   •   0 min focus time",
            font=("Segoe UI", 11, "bold"),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        )

        self.info_label.pack(
            side="left",
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
            values=values,
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
                1,
            )[1]

            self.selected_task_label.configure(
                text=f"Studying: {task_name}",
            )

        else:

            self.selected_task_label.configure(
                text="No task selected",
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

        # Do not reset a running session.

        if self.timer_running:

            return

        self.work_minutes = work
        self.break_minutes = break_time

        self.mode = "Focus"

        self.remaining_seconds = (
            self.work_minutes * 60
        )

        self.update_mode_visuals()

        self.start_button.configure(
            text="▶  Start Focus"
        )

        self.update_timer_label()

    # =========================================================
    # START / PAUSE
    # =========================================================

    def start_pause(self):

        if self.timer_running:

            self.timer_running = False

            if self.after_id is not None:

                try:

                    self.after_cancel(
                        self.after_id
                    )

                except Exception:
                    pass

                self.after_id = None

            self.start_button.configure(
                text=(
                    "▶  Resume"
                    if self.mode == "Focus"
                    else "▶  Resume Break"
                )
            )

            return

        self.timer_running = True

        self.start_button.configure(
            text="Ⅱ  Pause"
        )

        self.run_timer()

    # =========================================================
    # RUN TIMER
    # =========================================================

    def run_timer(self):

        if not self.timer_running:

            return

        self.update_timer_label()
        self.update_timer_progress()

        if self.remaining_seconds <= 0:

            self.timer_finished()

            return

        self.remaining_seconds -= 1

        self.after_id = self.after(
            1000,
            self.run_timer,
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

            self.update_mode_visuals()

            self.start_button.configure(
                text="▶  Start Break"
            )

        # -----------------------------------------------------
        # BREAK FINISHED
        # -----------------------------------------------------

        else:

            self.mode = "Focus"

            self.remaining_seconds = (
                self.work_minutes * 60
            )

            self.update_mode_visuals()

            self.start_button.configure(
                text="▶  Start Focus"
            )

        self.update_timer_label()
        self.update_timer_progress()

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

        self.update_mode_visuals()

        self.start_button.configure(
            text="▶  Start Focus"
        )

        self.update_timer_label()
        self.update_timer_progress()

    # =========================================================
    # TIMER DISPLAY
    # =========================================================

    def update_timer_label(self):

        minutes = (
            self.remaining_seconds // 60
        )

        seconds = (
            self.remaining_seconds % 60
        )

        self.timer_label.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

    # =========================================================
    # TIMER PROGRESS
    # =========================================================

    def update_timer_progress(self):

        if self.mode == "Focus":

            total = (
                self.work_minutes * 60
            )

        else:

            total = (
                self.break_minutes * 60
            )

        if total <= 0:

            self.timer_progress.set(0)

            return

        elapsed = total - self.remaining_seconds

        progress = elapsed / total

        self.timer_progress.set(
            max(
                0,
                min(
                    1,
                    progress,
                ),
            )
        )

    # =========================================================
    # MODE VISUALS
    # =========================================================

    def update_mode_visuals(self):

        if self.mode == "Focus":

            self.mode_badge.configure(
                fg_color=(
                    "#DBEAFE",
                    "#173252",
                )
            )

            self.mode_label.configure(
                text="●  FOCUS",
                text_color=(
                    "#2563EB",
                    "#60A5FA",
                ),
            )

            self.timer_progress.configure(
                progress_color=(
                    "#3B82F6",
                    "#3B82F6",
                )
            )

        else:

            self.mode_badge.configure(
                fg_color=(
                    "#DCFCE7",
                    "#16372A",
                )
            )

            self.mode_label.configure(
                text="●  BREAK",
                text_color=(
                    "#15803D",
                    "#4ADE80",
                ),
            )

            self.timer_progress.configure(
                progress_color=(
                    "#22C55E",
                    "#22C55E",
                )
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
                0,
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
                0,
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
        # 7. Notify
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
        # 8. Refresh dashboard
        # -----------------------------------------------------

        if hasattr(
            self.app,
            "refresh_dashboard",
        ):

            self.app.refresh_dashboard()

    # =========================================================
    # ACHIEVEMENT NAMES
    # =========================================================

    def get_achievement_names(
        self,
        achievement_ids,
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
        message,
    ):

        notification = ctk.CTkToplevel(
            self
        )

        notification.title(
            title
        )

        notification.geometry(
            "395x225"
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
            wraplength=330,
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
    # SESSION INFO
    # =========================================================

    def refresh_session_info(self):

        data = load_study_data()

        today = date.today().isoformat()

        sessions = data.get(
            "pomodoro_sessions",
            {},
        )

        count = sessions.get(
            today,
            0,
        )

        total_minutes = data.get(
            "total_focus_minutes",
            0,
        )

        self.info_label.configure(
            text=(
                f"{count} sessions"
                f"   •   "
                f"{total_minutes} min focus time"
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