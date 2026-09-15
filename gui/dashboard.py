import customtkinter as ctk

from core.task_manager import (
    load_tasks,
    get_statistics,
    get_streak,
    get_daily_goal_progress,
    load_study_data
)

from core.gamification import (
    get_gamification_summary,
    get_achievements
)


class DashboardView(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        app
    ):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.app = app

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.build()

    # ========================================================
    # BUILD DASHBOARD
    # ========================================================

    def build(self):

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
            0
        )

        achievements = get_achievements()

        unlocked_achievements = [
            achievement
            for achievement in achievements
            if achievement.get("unlocked")
        ]

        # ----------------------------------------------------
        # WELCOME
        # ----------------------------------------------------

        welcome = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#172554"
        )

        welcome.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            welcome,
            text="Welcome back, Student 👋",
            font=("Arial", 26, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            welcome,
            text=(
                "Stay consistent today and keep "
                "building your academic progress."
            ),
            font=("Arial", 13),
            text_color="#bfdbfe"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 22)
        )

        # ----------------------------------------------------
        # TOP STATISTICS
        # ----------------------------------------------------

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=(18, 5)
        )

        for column in range(6):

            stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.stat_card(
            stats_frame,
            0,
            "📚",
            stats["total"],
            "Total Tasks",
            "#2563eb"
        )

        self.stat_card(
            stats_frame,
            1,
            "✅",
            stats["completed"],
            "Completed",
            "#16a34a"
        )

        self.stat_card(
            stats_frame,
            2,
            "⏳",
            stats["pending"],
            "Pending",
            "#ca8a04"
        )

        self.stat_card(
            stats_frame,
            3,
            "🔴",
            stats["overdue"],
            "Overdue",
            "#dc2626"
        )

        self.stat_card(
            stats_frame,
            4,
            "🔥",
            streak,
            "Study Streak",
            "#ea580c"
        )

        self.stat_card(
            stats_frame,
            5,
            "⭐",
            gamification["xp"],
            "Total XP",
            "#7c3aed"
        )

        # ----------------------------------------------------
        # LEVEL + XP
        # ----------------------------------------------------

        level_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#1e293b"
        )

        level_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        level_header = ctk.CTkFrame(
            level_card,
            fg_color="transparent"
        )

        level_header.pack(
            fill="x",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            level_header,
            text=f"⭐ Level {gamification['level']}",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            level_header,
            text=(
                f"{gamification['progress_xp']} / 500 XP"
            ),
            font=("Arial", 14, "bold"),
            text_color="#c4b5fd"
        ).pack(
            side="right"
        )

        xp_bar = ctk.CTkProgressBar(
            level_card,
            height=14,
            corner_radius=8,
            progress_color="#7c3aed"
        )

        xp_bar.pack(
            fill="x",
            padx=20,
            pady=(8, 5)
        )

        xp_bar.set(
            gamification["percentage"] / 100
        )

        ctk.CTkLabel(
            level_card,
            text=(
                f"{gamification['xp']} total XP  •  "
                f"{gamification['achievements']} / "
                f"{gamification['total_achievements']} achievements unlocked"
            ),
            font=("Arial", 11),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 20)
        )

        # ----------------------------------------------------
        # OVERALL PROGRESS
        # ----------------------------------------------------

        progress_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#1e293b"
        )

        progress_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        title_row = ctk.CTkFrame(
            progress_card,
            fg_color="transparent"
        )

        title_row.pack(
            fill="x",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            title_row,
            text="📊 Overall Study Progress",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            title_row,
            text=f"{stats['progress']}%",
            font=("Arial", 20, "bold"),
            text_color="#60a5fa"
        ).pack(
            side="right"
        )

        progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=16,
            corner_radius=8,
            progress_color="#3b82f6"
        )

        progress_bar.pack(
            fill="x",
            padx=20,
            pady=(8, 5)
        )

        progress_bar.set(
            stats["progress"] / 100
        )

        ctk.CTkLabel(
            progress_card,
            text=(
                f"{stats['completed']} of "
                f"{stats['total']} tasks completed"
            ),
            font=("Arial", 11),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        # ----------------------------------------------------
        # DAILY GOAL
        # ----------------------------------------------------

        goal_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#1e293b"
        )

        goal_card.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            goal_card,
            text="🎯 Today's Study Goal",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            goal_card,
            text=(
                f"{daily_goal['completed']} / "
                f"{daily_goal['goal']} tasks completed today"
            ),
            font=("Arial", 14, "bold"),
            text_color="#fbbf24"
        ).pack(
            anchor="w",
            padx=20
        )

        goal_bar = ctk.CTkProgressBar(
            goal_card,
            height=13,
            corner_radius=8,
            progress_color="#f59e0b"
        )

        goal_bar.pack(
            fill="x",
            padx=20,
            pady=(10, 5)
        )

        goal_bar.set(
            daily_goal["percentage"] / 100
        )

        if daily_goal["percentage"] >= 100:

            goal_message = (
                "🎉 Daily goal completed! Excellent work."
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
            font=("Arial", 11),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # WORKLOAD + FOCUS
        # ----------------------------------------------------

        workload_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        workload_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        workload_frame.grid_columnconfigure(
            0,
            weight=1
        )

        workload_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # Workload
        workload_card = ctk.CTkFrame(
            workload_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        workload_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        ctk.CTkLabel(
            workload_card,
            text="⏱️ Remaining Study Workload",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 6)
        )

        workload_text = self.format_minutes(
            stats["estimated_minutes"]
        )

        ctk.CTkLabel(
            workload_card,
            text=workload_text,
            font=("Arial", 30, "bold"),
            text_color="#a78bfa"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            workload_card,
            text="Estimated remaining time",
            font=("Arial", 12),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 20)
        )

        # Focus
        focus_card = ctk.CTkFrame(
            workload_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        focus_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        ctk.CTkLabel(
            focus_card,
            text="🧠 Focus Time",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 6)
        )

        focus_text = self.format_minutes(
            focus_minutes
        )

        ctk.CTkLabel(
            focus_card,
            text=focus_text,
            font=("Arial", 30, "bold"),
            text_color="#22c55e"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            focus_card,
            text=(
                f"{gamification['sessions']} focus "
                "session(s) completed"
            ),
            font=("Arial", 12),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 20)
        )

        # ----------------------------------------------------
        # ACHIEVEMENTS
        # ----------------------------------------------------

        achievement_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#1e293b"
        )

        achievement_card.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            achievement_card,
            text="🏆 Recent Achievements",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        if unlocked_achievements:

            for achievement in unlocked_achievements[-3:]:

                row = ctk.CTkFrame(
                    achievement_card,
                    fg_color="transparent"
                )

                row.pack(
                    fill="x",
                    padx=20,
                    pady=4
                )

                ctk.CTkLabel(
                    row,
                    text=achievement["icon"],
                    font=("Arial", 20),
                    width=35
                ).pack(
                    side="left"
                )

                text_frame = ctk.CTkFrame(
                    row,
                    fg_color="transparent"
                )

                text_frame.pack(
                    side="left",
                    fill="x",
                    expand=True
                )

                ctk.CTkLabel(
                    text_frame,
                    text=achievement["name"],
                    font=("Arial", 13, "bold"),
                    text_color="#f8fafc"
                ).pack(
                    anchor="w"
                )

                ctk.CTkLabel(
                    text_frame,
                    text=achievement["description"],
                    font=("Arial", 10),
                    text_color="#94a3b8"
                ).pack(
                    anchor="w"
                )

        else:

            ctk.CTkLabel(
                achievement_card,
                text=(
                    "No achievements unlocked yet.\n"
                    "Complete tasks and focus sessions to earn them!"
                ),
                font=("Arial", 12),
                text_color="#94a3b8",
                justify="left"
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 20)
            )

        # ----------------------------------------------------
        # QUICK ACTIONS
        # ----------------------------------------------------

        action_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#1e293b"
        )

        action_card.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            action_card,
            text="⚡ Quick Actions",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        buttons = ctk.CTkFrame(
            action_card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        ctk.CTkButton(
            buttons,
            text="➕ Add Task",
            width=140,
            height=42,
            corner_radius=10,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.app.show_tasks
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            buttons,
            text="📝 View Tasks",
            width=140,
            height=42,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.app.show_tasks
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text="🍅 Focus",
            width=140,
            height=42,
            corner_radius=10,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.app.show_focus
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text="🏆 Achievements",
            width=160,
            height=42,
            corner_radius=10,
            fg_color="#ca8a04",
            hover_color="#a16207",
            command=self.app.show_achievements
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text="📊 Analytics",
            width=140,
            height=42,
            corner_radius=10,
            fg_color="#0891b2",
            hover_color="#0e7490",
            command=self.app.show_analytics
        ).pack(
            side="left",
            padx=10
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def stat_card(
        self,
        parent,
        column,
        icon,
        value,
        label,
        accent
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 4)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 26, "bold"),
            text_color=accent
        ).pack(
            anchor="w",
            padx=15
        )

        ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 11),
            text_color="#94a3b8"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

    # ========================================================
    # FORMAT MINUTES
    # ========================================================

    def format_minutes(
        self,
        minutes
    ):

        try:
            minutes = int(
                minutes
            )
        except (
            ValueError,
            TypeError
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