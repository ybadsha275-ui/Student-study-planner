import customtkinter as ctk

from core.task_manager import (
    load_tasks,
    get_statistics,
    get_streak,
    get_daily_goal_progress,
    load_study_data,
)

from core.gamification import (
    get_gamification_summary,
    get_achievements,
)


class DashboardView(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
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

        self.build()

    # =========================================================
    # BUILD DASHBOARD
    # =========================================================

    def build(self):

        # -----------------------------------------------------
        # LOAD DATA
        # -----------------------------------------------------

        tasks = load_tasks()

        stats = get_statistics(
            tasks
        )

        gamification = get_gamification_summary()

        daily_goal = get_daily_goal_progress()

        study_data = load_study_data()

        streak = get_streak()

        focus_minutes = study_data.get(
            "total_focus_minutes",
            0,
        )

        achievements = get_achievements()

        unlocked_achievements = [
            achievement
            for achievement in achievements
            if achievement.get("unlocked")
        ]

        # -----------------------------------------------------
        # MAIN CONTENT
        # -----------------------------------------------------

        content = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        content.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=8,
        )

        content.grid_columnconfigure(
            0,
            weight=1,
        )

        # =====================================================
        # WELCOME BANNER
        # =====================================================

        welcome = ctk.CTkFrame(
            content,
            corner_radius=22,
            fg_color=(
                "#EAF2FF",
                "#16243A",
            ),
            border_width=1,
            border_color=(
                "#D6E5FF",
                "#243A59",
            ),
        )

        welcome.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        welcome.grid_columnconfigure(
            0,
            weight=1,
        )

        welcome_text = ctk.CTkFrame(
            welcome,
            fg_color="transparent",
        )

        welcome_text.grid(
            row=0,
            column=0,
            sticky="w",
            padx=26,
            pady=24,
        )

        ctk.CTkLabel(
            welcome_text,
            text="WELCOME BACK",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                "#2563EB",
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            welcome_text,
            text="Ready to make progress today? 👋",
            font=("Segoe UI", 27, "bold"),
            text_color=(
                "#111827",
                "#F8FAFC",
            ),
        ).pack(
            anchor="w",
            pady=(3, 4),
        )

        ctk.CTkLabel(
            welcome_text,
            text=(
                "Stay consistent, complete your priorities, "
                "and keep building your academic momentum."
            ),
            font=("Segoe UI", 12),
            text_color=(
                "#526174",
                "#A8B4C4",
            ),
        ).pack(
            anchor="w",
        )

        # Small right-side visual
        welcome_badge = ctk.CTkFrame(
            welcome,
            width=110,
            height=90,
            corner_radius=18,
            fg_color=(
                "#DCEBFF",
                "#1D3555",
            ),
        )

        welcome_badge.grid(
            row=0,
            column=1,
            padx=24,
            pady=18,
        )

        welcome_badge.grid_propagate(False)

        ctk.CTkLabel(
            welcome_badge,
            text="FOCUS",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                "#4B6480",
                "#A7BBD4",
            ),
        ).pack(
            pady=(14, 0),
        )

        ctk.CTkLabel(
            welcome_badge,
            text="TODAY",
            font=("Segoe UI", 16, "bold"),
            text_color=(
                "#2563EB",
                "#60A5FA",
            ),
        ).pack()

        # =====================================================
        # STATISTICS
        # =====================================================

        stats_frame = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )

        stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        for column in range(6):
            stats_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        self.stat_card(
            stats_frame,
            0,
            "📚",
            stats["total"],
            "Total Tasks",
            "#3B82F6",
            "Everything planned",
        )

        self.stat_card(
            stats_frame,
            1,
            "✓",
            stats["completed"],
            "Completed",
            "#22C55E",
            "Finished successfully",
        )

        self.stat_card(
            stats_frame,
            2,
            "◷",
            stats["pending"],
            "Pending",
            "#F59E0B",
            "Still on your list",
        )

        self.stat_card(
            stats_frame,
            3,
            "!",
            stats["overdue"],
            "Overdue",
            "#EF4444",
            "Needs attention",
        )

        self.stat_card(
            stats_frame,
            4,
            "🔥",
            streak,
            "Study Streak",
            "#F97316",
            "Keep the momentum",
        )

        self.stat_card(
            stats_frame,
            5,
            "★",
            gamification["xp"],
            "Total XP",
            "#8B5CF6",
            "Academic progress",
        )

        # =====================================================
        # LEVEL + XP
        # =====================================================

        level_card = self.create_card(
            content,
            row=2,
            pady=(0, 16),
        )

        level_header = ctk.CTkFrame(
            level_card,
            fg_color="transparent",
        )

        level_header.pack(
            fill="x",
            padx=22,
            pady=(20, 8),
        )

        level_left = ctk.CTkFrame(
            level_header,
            fg_color="transparent",
        )

        level_left.pack(
            side="left",
        )

        ctk.CTkLabel(
            level_left,
            text="LEVEL PROGRESS",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            level_left,
            text=f"⭐ Level {gamification['level']}",
            font=("Segoe UI", 20, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        ctk.CTkLabel(
            level_header,
            text=f"{gamification['progress_xp']} / 500 XP",
            font=("Segoe UI", 14, "bold"),
            text_color=(
                "#7C3AED",
                "#A78BFA",
            ),
        ).pack(
            side="right",
            anchor="s",
        )

        xp_bar = ctk.CTkProgressBar(
            level_card,
            height=13,
            corner_radius=7,
            progress_color=(
                "#8B5CF6",
                "#8B5CF6",
            ),
            fg_color=(
                "#E5E7EB",
                "#2A3441",
            ),
        )

        xp_bar.pack(
            fill="x",
            padx=22,
            pady=(2, 8),
        )

        xp_bar.set(
            max(
                0,
                min(
                    1,
                    gamification["percentage"] / 100,
                ),
            )
        )

        ctk.CTkLabel(
            level_card,
            text=(
                f"{gamification['xp']} total XP   •   "
                f"{gamification['achievements']} / "
                f"{gamification['total_achievements']} "
                "achievements unlocked"
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(2, 20),
        )

        # =====================================================
        # OVERALL PROGRESS
        # =====================================================

        progress_card = self.create_card(
            content,
            row=3,
            pady=(0, 16),
        )

        self.section_heading(
            progress_card,
            "OVERALL PROGRESS",
            "📊",
            f"{stats['progress']}%",
        )

        progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=14,
            corner_radius=7,
            progress_color=(
                "#3B82F6",
                "#3B82F6",
            ),
            fg_color=(
                "#E5E7EB",
                "#2A3441",
            ),
        )

        progress_bar.pack(
            fill="x",
            padx=22,
            pady=(12, 7),
        )

        progress_bar.set(
            max(
                0,
                min(
                    1,
                    stats["progress"] / 100,
                ),
            )
        )

        ctk.CTkLabel(
            progress_card,
            text=(
                f"{stats['completed']} of "
                f"{stats['total']} tasks completed"
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 20),
        )

        # =====================================================
        # DAILY GOAL
        # =====================================================

        goal_card = self.create_card(
            content,
            row=4,
            pady=(0, 16),
        )

        self.section_heading(
            goal_card,
            "TODAY'S STUDY GOAL",
            "🎯",
            f"{daily_goal['completed']} / {daily_goal['goal']}",
        )

        ctk.CTkLabel(
            goal_card,
            text=(
                f"{daily_goal['completed']} of "
                f"{daily_goal['goal']} planned tasks completed"
            ),
            font=("Segoe UI", 13, "bold"),
            text_color=(
                "#92400E",
                "#FBBF24",
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(2, 4),
        )

        goal_bar = ctk.CTkProgressBar(
            goal_card,
            height=13,
            corner_radius=7,
            progress_color=(
                "#F59E0B",
                "#F59E0B",
            ),
            fg_color=(
                "#F3F4F6",
                "#2A3441",
            ),
        )

        goal_bar.pack(
            fill="x",
            padx=22,
            pady=(9, 8),
        )

        goal_bar.set(
            max(
                0,
                min(
                    1,
                    daily_goal["percentage"] / 100,
                ),
            )
        )

        if daily_goal["percentage"] >= 100:

            goal_message = (
                "🎉 Goal completed — excellent work today!"
            )

        elif daily_goal["completed"] == 0:

            goal_message = (
                "Start with one task and build momentum."
            )

        else:

            remaining = (
                daily_goal["goal"]
                - daily_goal["completed"]
            )

            goal_message = (
                f"{remaining} task(s) remaining "
                "to reach today's goal."
            )

        ctk.CTkLabel(
            goal_card,
            text=goal_message,
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 20),
        )

        # =====================================================
        # WORKLOAD + FOCUS
        # =====================================================

        metrics_frame = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )

        metrics_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        metrics_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        metrics_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # WORKLOAD CARD
        # -----------------------------------------------------

        workload_card = self.create_card(
            metrics_frame,
            row=0,
            column=0,
            padx=(0, 7),
        )

        ctk.CTkLabel(
            workload_card,
            text="⏱",
            font=("Segoe UI Symbol", 22),
            text_color=(
                "#7C3AED",
                "#A78BFA",
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 4),
        )

        ctk.CTkLabel(
            workload_card,
            text="Remaining Study Workload",
            font=("Segoe UI", 16, "bold"),
        ).pack(
            anchor="w",
            padx=22,
        )

        workload_text = self.format_minutes(
            stats["estimated_minutes"]
        )

        ctk.CTkLabel(
            workload_card,
            text=workload_text,
            font=("Segoe UI", 31, "bold"),
            text_color=(
                "#7C3AED",
                "#A78BFA",
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(7, 0),
        )

        ctk.CTkLabel(
            workload_card,
            text="Estimated time remaining",
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(1, 20),
        )

        # -----------------------------------------------------
        # FOCUS CARD
        # -----------------------------------------------------

        focus_card = self.create_card(
            metrics_frame,
            row=0,
            column=1,
            padx=(7, 0),
        )

        ctk.CTkLabel(
            focus_card,
            text="🧠",
            font=("Segoe UI", 22),
            text_color=(
                "#16A34A",
                "#4ADE80",
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 4),
        )

        ctk.CTkLabel(
            focus_card,
            text="Focus Time",
            font=("Segoe UI", 16, "bold"),
        ).pack(
            anchor="w",
            padx=22,
        )

        focus_text = self.format_minutes(
            focus_minutes
        )

        ctk.CTkLabel(
            focus_card,
            text=focus_text,
            font=("Segoe UI", 31, "bold"),
            text_color=(
                "#16A34A",
                "#4ADE80",
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(7, 0),
        )

        ctk.CTkLabel(
            focus_card,
            text=(
                f"{gamification['sessions']} focus "
                "session(s) completed"
            ),
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=22,
            pady=(1, 20),
        )

        # =====================================================
        # ACHIEVEMENTS
        # =====================================================

        achievement_card = self.create_card(
            content,
            row=6,
            pady=(0, 16),
        )

        self.section_heading(
            achievement_card,
            "RECENT ACHIEVEMENTS",
            "🏆",
            f"{len(unlocked_achievements)} unlocked",
        )

        if unlocked_achievements:

            recent = unlocked_achievements[-3:]
            recent.reverse()

            for achievement in recent:

                self.achievement_row(
                    achievement_card,
                    achievement,
                )

        else:

            empty_frame = ctk.CTkFrame(
                achievement_card,
                corner_radius=12,
                fg_color=(
                    "#F7F8FA",
                    "#202833",
                ),
            )

            empty_frame.pack(
                fill="x",
                padx=22,
                pady=(3, 20),
            )

            ctk.CTkLabel(
                empty_frame,
                text="🏆",
                font=("Segoe UI", 23),
            ).pack(
                side="left",
                padx=(16, 10),
                pady=15,
            )

            ctk.CTkLabel(
                empty_frame,
                text=(
                    "No achievements unlocked yet. "
                    "Complete tasks and focus sessions to earn them!"
                ),
                font=("Segoe UI", 11),
                text_color=(
                    self.colors["muted_light"],
                    self.colors["muted_dark"],
                ),
                justify="left",
                wraplength=700,
            ).pack(
                side="left",
                pady=15,
            )

        # =====================================================
        # QUICK ACTIONS
        # =====================================================

        action_card = self.create_card(
            content,
            row=7,
            pady=(0, 20),
        )

        self.section_heading(
            action_card,
            "QUICK ACTIONS",
            "⚡",
            "Jump right in",
        )

        buttons = ctk.CTkFrame(
            action_card,
            fg_color="transparent",
        )

        buttons.pack(
            fill="x",
            padx=22,
            pady=(4, 20),
        )

        action_specs = [
            (
                "➕  Add Task",
                "#16A34A",
                "#15803D",
                self.app.show_tasks,
            ),
            (
                "📝  View Tasks",
                "#3B82F6",
                "#2563EB",
                self.app.show_tasks,
            ),
            (
                "🍅  Focus",
                "#7C3AED",
                "#6D28D9",
                self.app.show_focus,
            ),
            (
                "🏆  Achievements",
                "#CA8A04",
                "#A16207",
                self.app.show_achievements,
            ),
            (
                "📊  Analytics",
                "#0891B2",
                "#0E7490",
                self.app.show_analytics,
            ),
        ]

        for index, (
            text,
            fg,
            hover,
            command,
        ) in enumerate(action_specs):

            button = ctk.CTkButton(
                buttons,
                text=text,
                height=42,
                corner_radius=11,
                font=("Segoe UI", 11, "bold"),
                fg_color=fg,
                hover_color=hover,
                command=command,
            )

            button.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=5,
            )

            buttons.grid_columnconfigure(
                index,
                weight=1,
            )

        # =====================================================
        # END
        # =====================================================

        # Give a little breathing room at the bottom.
        content.grid_rowconfigure(
            8,
            minsize=10,
        )

    # =========================================================
    # CREATE CARD
    # =========================================================

    def create_card(
        self,
        parent,
        row,
        column=0,
        padx=None,
        pady=None,
    ):

        card = ctk.CTkFrame(
            parent,
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

        if column == 0 and parent == self:

            column = 0

        grid_kwargs = {
            "row": row,
            "column": column,
            "sticky": "ew",
        }

        if padx is not None:
            grid_kwargs["padx"] = padx

        if pady is not None:
            grid_kwargs["pady"] = pady

        card.grid(
            **grid_kwargs,
        )

        if isinstance(
            parent,
            ctk.CTkFrame,
        ):

            try:
                parent.grid_columnconfigure(
                    column,
                    weight=1,
                )
            except Exception:
                pass

        return card

    # =========================================================
    # SECTION HEADING
    # =========================================================

    def section_heading(
        self,
        parent,
        title,
        icon,
        value,
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        row.pack(
            fill="x",
            padx=22,
            pady=(18, 3),
        )

        left = ctk.CTkFrame(
            row,
            fg_color="transparent",
        )

        left.pack(
            side="left",
        )

        ctk.CTkLabel(
            left,
            text=icon,
            font=("Segoe UI", 18),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ctk.CTkLabel(
            left,
            text=title,
            font=("Segoe UI", 16, "bold"),
        ).pack(
            side="left",
        )

        ctk.CTkLabel(
            row,
            text=str(value),
            font=("Segoe UI", 15, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            side="right",
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def stat_card(
        self,
        parent,
        column,
        icon,
        value,
        label,
        accent,
        description,
    ):

        card = ctk.CTkFrame(
            parent,
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
            padx=14,
            pady=(13, 5),
        )

        icon_box = ctk.CTkFrame(
            top,
            width=34,
            height=34,
            corner_radius=9,
            fg_color=(
                "#F3F6FA",
                "#202833",
            ),
        )

        icon_box.pack(
            side="left",
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Segoe UI", 15, "bold"),
            text_color=accent,
        ).pack(
            expand=True,
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 25, "bold"),
            text_color=accent,
        ).pack(
            anchor="w",
            padx=14,
        )

        ctk.CTkLabel(
            card,
            text=label,
            font=("Segoe UI", 11, "bold"),
        ).pack(
            anchor="w",
            padx=14,
            pady=(0, 1),
        )

        ctk.CTkLabel(
            card,
            text=description,
            font=("Segoe UI", 9),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            padx=14,
            pady=(0, 13),
        )

    # =========================================================
    # ACHIEVEMENT ROW
    # =========================================================

    def achievement_row(
        self,
        parent,
        achievement,
    ):

        row = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=(
                "#F7F8FA",
                "#202833",
            ),
        )

        row.pack(
            fill="x",
            padx=22,
            pady=4,
        )

        ctk.CTkLabel(
            row,
            text=achievement["icon"],
            font=("Segoe UI", 22),
            width=40,
        ).pack(
            side="left",
            padx=(13, 5),
            pady=12,
        )

        text_frame = ctk.CTkFrame(
            row,
            fg_color="transparent",
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
            pady=10,
        )

        ctk.CTkLabel(
            text_frame,
            text=achievement["name"],
            font=("Segoe UI", 12, "bold"),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            text_frame,
            text=achievement["description"],
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        ctk.CTkLabel(
            row,
            text="UNLOCKED",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                "#15803D",
                "#4ADE80",
            ),
        ).pack(
            side="right",
            padx=15,
        )

    # =========================================================
    # FORMAT MINUTES
    # =========================================================

    def format_minutes(
        self,
        minutes,
    ):

        try:

            minutes = int(
                minutes
            )

        except (
            ValueError,
            TypeError,
        ):

            minutes = 0

        hours = minutes // 60

        remaining = minutes % 60

        if hours > 0:

            if remaining > 0:

                return (
                    f"{hours}h "
                    f"{remaining}m"
                )

            return f"{hours}h"

        return f"{remaining} min"