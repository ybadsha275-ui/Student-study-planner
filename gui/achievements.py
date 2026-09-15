import customtkinter as ctk

from core.gamification import (
    get_gamification_summary,
    get_achievements,
    check_achievements
)


class AchievementsView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        app
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.app = app

        # Check for newly unlocked achievements
        check_achievements()

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.create_header()
        self.create_profile_card()
        self.create_achievements_section()

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
            text="Achievements",
            font=("Segoe UI", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Build consistency, earn XP and unlock achievements.",
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
            text="Refresh",
            width=100,
            command=self.refresh_page
        ).grid(
            row=0,
            column=1,
            rowspan=2
        )

    # =========================================================
    # LEVEL / XP PROFILE
    # =========================================================

    def create_profile_card(self):

        self.profile_card = ctk.CTkFrame(
            self,
            corner_radius=18
        )

        self.profile_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        self.profile_card.grid_columnconfigure(
            1,
            weight=1
        )

        self.build_profile_contents()

    def build_profile_contents(self):

        for widget in self.profile_card.winfo_children():
            widget.destroy()

        data = get_gamification_summary()

        # -----------------------------------------------------
        # Level
        # -----------------------------------------------------

        level_frame = ctk.CTkFrame(
            self.profile_card,
            fg_color="transparent"
        )

        level_frame.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            level_frame,
            text="⭐",
            font=("Segoe UI", 36)
        ).pack()

        ctk.CTkLabel(
            level_frame,
            text=f"LEVEL {data['level']}",
            font=("Segoe UI", 21, "bold")
        ).pack(
            pady=(3, 0)
        )

        # -----------------------------------------------------
        # XP
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.profile_card,
            text=f"{data['xp']} XP",
            font=("Segoe UI", 21, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=10,
            pady=(20, 3)
        )

        ctk.CTkLabel(
            self.profile_card,
            text=(
                f"{data['progress_xp']} / 500 XP "
                f"toward next level"
            ),
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65")
        ).grid(
            row=0,
            column=2,
            sticky="e",
            padx=20,
            pady=(20, 3)
        )

        # -----------------------------------------------------
        # XP Progress
        # -----------------------------------------------------

        progress = ctk.CTkProgressBar(
            self.profile_card,
            height=13
        )

        progress.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(3, 5)
        )

        progress.set(
            data["percentage"] / 100
        )

        # -----------------------------------------------------
        # Achievement count
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.profile_card,
            text=(
                f"🏆 {data['achievements']} / "
                f"{data['total_achievements']} unlocked"
            ),
            font=("Segoe UI", 11, "bold")
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=10,
            pady=(0, 18)
        )

        achievement_percent = (
            round(
                (
                    data["achievements"]
                    / data["total_achievements"]
                ) * 100
            )
            if data["total_achievements"]
            else 0
        )

        ctk.CTkLabel(
            self.profile_card,
            text=f"{achievement_percent}% complete",
            font=("Segoe UI", 11),
            text_color=("gray45", "gray65")
        ).grid(
            row=2,
            column=2,
            sticky="e",
            padx=20,
            pady=(0, 18)
        )

    # =========================================================
    # ACHIEVEMENTS
    # =========================================================

    def create_achievements_section(self):

        self.achievement_container = ctk.CTkScrollableFrame(
            self,
            corner_radius=15
        )

        self.achievement_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(5, 20)
        )

        self.build_achievements()

    def build_achievements(self):

        for widget in self.achievement_container.winfo_children():
            widget.destroy()

        achievements = get_achievements()

        unlocked = [
            item
            for item in achievements
            if item.get("unlocked", False)
        ]

        locked = [
            item
            for item in achievements
            if not item.get("unlocked", False)
        ]

        # -----------------------------------------------------
        # Unlocked
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.achievement_container,
            text="Unlocked Achievements",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        if unlocked:

            for achievement in unlocked:
                self.create_achievement_card(
                    achievement,
                    True
                )

        else:

            ctk.CTkLabel(
                self.achievement_container,
                text=(
                    "No achievements unlocked yet.\n"
                    "Complete tasks and focus sessions to begin!"
                ),
                font=("Segoe UI", 13),
                text_color=("gray45", "gray65"),
                justify="left"
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 20)
            )

        # -----------------------------------------------------
        # Locked
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.achievement_container,
            text="Achievements to Unlock",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        if locked:

            for achievement in locked:
                self.create_achievement_card(
                    achievement,
                    False
                )

        else:

            ctk.CTkLabel(
                self.achievement_container,
                text="🎉 You have unlocked every achievement!",
                font=("Segoe UI", 14, "bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 20)
            )

    # =========================================================
    # ACHIEVEMENT CARD
    # =========================================================

    def create_achievement_card(
        self,
        achievement,
        unlocked
    ):

        card = ctk.CTkFrame(
            self.achievement_container,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=8,
            pady=5
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # Icon
        # -----------------------------------------------------

        icon = (
            achievement.get(
                "icon",
                "🏆"
            )
            if unlocked
            else "🔒"
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI", 30),
            width=60
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=15,
            pady=15
        )

        # -----------------------------------------------------
        # Name / description
        # -----------------------------------------------------

        ctk.CTkLabel(
            card,
            text=achievement.get(
                "name",
                "Achievement"
            ),
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=10,
            pady=(15, 2)
        )

        ctk.CTkLabel(
            card,
            text=achievement.get(
                "description",
                ""
            ),
            font=("Segoe UI", 11),
            text_color=("gray40", "gray65"),
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=10,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        if unlocked:

            status = "✓ UNLOCKED"

        else:

            status = "LOCKED"

        ctk.CTkLabel(
            card,
            text=status,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=20
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_page(self):

        check_achievements()

        self.build_profile_contents()
        self.build_achievements()