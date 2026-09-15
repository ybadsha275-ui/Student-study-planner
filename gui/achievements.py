import customtkinter as ctk

from core.gamification import (
    get_gamification_summary,
    get_achievements,
    check_achievements,
)


class AchievementsView(ctk.CTkFrame):

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
        # CHECK ACHIEVEMENTS
        # =====================================================

        check_achievements()

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
        self.create_profile_card()
        self.create_achievements_section()

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
            text="PROGRESS & REWARDS",
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
            text="Achievements",
            font=("Segoe UI", 30, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            heading,
            text="Build consistency, earn XP and unlock achievements.",
            font=("Segoe UI", 12),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

        # -----------------------------------------------------
        # REFRESH
        # -----------------------------------------------------

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=105,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            command=self.refresh_page,
        ).grid(
            row=0,
            column=1,
            padx=(15, 0),
        )

    # =========================================================
    # PROFILE CARD
    # =========================================================

    def create_profile_card(self):

        self.profile_card = ctk.CTkFrame(
            self,
            corner_radius=20,
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

        self.profile_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 14),
        )

        self.build_profile_contents()

    # =========================================================
    # PROFILE CONTENT
    # =========================================================

    def build_profile_contents(self):

        for widget in self.profile_card.winfo_children():

            widget.destroy()

        data = get_gamification_summary()

        self.profile_card.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # LEVEL BADGE
        # -----------------------------------------------------

        level_box = ctk.CTkFrame(
            self.profile_card,
            width=125,
            height=120,
            corner_radius=18,
            fg_color=(
                "#EEF4FF",
                "#172A42",
            ),
        )

        level_box.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(18, 15),
            pady=18,
        )

        level_box.grid_propagate(
            False,
        )

        ctk.CTkLabel(
            level_box,
            text="⭐",
            font=("Segoe UI", 30),
            text_color=(
                "#D97706",
                "#FBBF24",
            ),
        ).pack(
            pady=(13, 0),
        )

        ctk.CTkLabel(
            level_box,
            text=f"LEVEL {data['level']}",
            font=("Segoe UI", 17, "bold"),
            text_color=(
                "#1D4ED8",
                "#60A5FA",
            ),
        ).pack(
            pady=(2, 0),
        )

        # -----------------------------------------------------
        # XP HEADER
        # -----------------------------------------------------

        xp_header = ctk.CTkFrame(
            self.profile_card,
            fg_color="transparent",
        )

        xp_header.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(5, 18),
            pady=(19, 4),
        )

        xp_header.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            xp_header,
            text="EXPERIENCE",
            font=("Segoe UI", 9, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            xp_header,
            text=f"{data['xp']} XP",
            font=("Segoe UI", 20, "bold"),
            text_color=(
                "#7C3AED",
                "#A78BFA",
            ),
        ).grid(
            row=1,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            xp_header,
            text=(
                f"{data['progress_xp']} / 500 XP "
                "toward next level"
            ),
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=1,
            column=1,
            sticky="e",
        )

        # -----------------------------------------------------
        # XP BAR
        # -----------------------------------------------------

        progress = ctk.CTkProgressBar(
            self.profile_card,
            height=12,
            corner_radius=6,
            progress_color=(
                "#8B5CF6",
                "#8B5CF6",
            ),
            fg_color=(
                "#E5E7EB",
                "#2A3441",
            ),
        )

        progress.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(5, 18),
            pady=(4, 8),
        )

        progress.set(
            max(
                0,
                min(
                    1,
                    data["percentage"] / 100,
                ),
            )
        )

        # -----------------------------------------------------
        # ACHIEVEMENT PROGRESS
        # -----------------------------------------------------

        achievements_completed = data[
            "achievements"
        ]

        total_achievements = data[
            "total_achievements"
        ]

        achievement_percent = (
            round(
                (
                    achievements_completed
                    / total_achievements
                )
                * 100
            )
            if total_achievements
            else 0
        )

        status = ctk.CTkFrame(
            self.profile_card,
            fg_color="transparent",
        )

        status.grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(5, 18),
            pady=(0, 17),
        )

        status.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            status,
            text=(
                f"🏆 {achievements_completed} / "
                f"{total_achievements} achievements unlocked"
            ),
            font=("Segoe UI", 10, "bold"),
            text_color=(
                "#15803D",
                "#4ADE80",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            status,
            text=f"{achievement_percent}% complete",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).grid(
            row=0,
            column=1,
            sticky="e",
        )

    # =========================================================
    # ACHIEVEMENT SECTION
    # =========================================================

    def create_achievements_section(self):

        self.achievement_container = ctk.CTkScrollableFrame(
            self,
            corner_radius=18,
            fg_color=(
                "#F5F7FA",
                "#111820",
            ),
        )

        self.achievement_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20),
        )

        self.achievement_container.grid_columnconfigure(
            0,
            weight=1,
        )

        self.build_achievements()

    # =========================================================
    # BUILD ACHIEVEMENTS
    # =========================================================

    def build_achievements(self):

        for widget in self.achievement_container.winfo_children():

            widget.destroy()

        achievements = get_achievements()

        unlocked = [
            item
            for item in achievements
            if item.get(
                "unlocked",
                False,
            )
        ]

        locked = [
            item
            for item in achievements
            if not item.get(
                "unlocked",
                False,
            )
        ]

        # -----------------------------------------------------
        # UNLOCKED HEADER
        # -----------------------------------------------------

        unlocked_header = ctk.CTkFrame(
            self.achievement_container,
            fg_color="transparent",
        )

        unlocked_header.pack(
            fill="x",
            padx=8,
            pady=(13, 7),
        )

        ctk.CTkLabel(
            unlocked_header,
            text="UNLOCKED ACHIEVEMENTS",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                "#15803D",
                "#4ADE80",
            ),
        ).pack(
            side="left",
        )

        ctk.CTkLabel(
            unlocked_header,
            text=str(len(unlocked)),
            font=("Segoe UI", 11, "bold"),
            text_color=(
                "#15803D",
                "#4ADE80",
            ),
        ).pack(
            side="right",
        )

        # -----------------------------------------------------
        # UNLOCKED
        # -----------------------------------------------------

        if unlocked:

            for achievement in unlocked:

                self.create_achievement_card(
                    achievement,
                    True,
                )

        else:

            self.create_empty_section(
                "No achievements unlocked yet.",
                "Complete tasks and focus sessions to start earning rewards.",
                "🎯",
            )

        # -----------------------------------------------------
        # LOCKED HEADER
        # -----------------------------------------------------

        locked_header = ctk.CTkFrame(
            self.achievement_container,
            fg_color="transparent",
        )

        locked_header.pack(
            fill="x",
            padx=8,
            pady=(22, 7),
        )

        ctk.CTkLabel(
            locked_header,
            text="ACHIEVEMENTS TO UNLOCK",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="left",
        )

        ctk.CTkLabel(
            locked_header,
            text=str(len(locked)),
            font=("Segoe UI", 11, "bold"),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            side="right",
        )

        # -----------------------------------------------------
        # LOCKED
        # -----------------------------------------------------

        if locked:

            for achievement in locked:

                self.create_achievement_card(
                    achievement,
                    False,
                )

        else:

            self.create_empty_section(
                "🎉 Every achievement is unlocked!",
                "You have completed the entire achievement collection.",
                "🏆",
            )

    # =========================================================
    # EMPTY SECTION
    # =========================================================

    def create_empty_section(
        self,
        title,
        description,
        icon,
    ):

        card = ctk.CTkFrame(
            self.achievement_container,
            corner_radius=15,
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

        card.pack(
            fill="x",
            padx=8,
            pady=(2, 6),
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI", 28),
        ).pack(
            pady=(21, 5),
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 15, "bold"),
        ).pack()

        ctk.CTkLabel(
            card,
            text=description,
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            pady=(3, 20),
        )

    # =========================================================
    # ACHIEVEMENT CARD
    # =========================================================

    def create_achievement_card(
        self,
        achievement,
        unlocked,
    ):

        if unlocked:

            card_fg = (
                "#FFFFFF",
                "#181F28",
            )

            icon_bg = (
                "#ECFDF5",
                "#16372A",
            )

            icon_color = (
                "#15803D",
                "#4ADE80",
            )

            status_bg = (
                "#DCFCE7",
                "#1B4330",
            )

            status_color = (
                "#15803D",
                "#4ADE80",
            )

        else:

            card_fg = (
                "#F5F6F8",
                "#171D25",
            )

            icon_bg = (
                "#E9EDF2",
                "#242C36",
            )

            icon_color = (
                "#64748B",
                "#7C8A99",
            )

            status_bg = (
                "#E9EDF2",
                "#242C36",
            )

            status_color = (
                "#64748B",
                "#8B95A5",
            )

        card = ctk.CTkFrame(
            self.achievement_container,
            corner_radius=16,
            fg_color=card_fg,
            border_width=1,
            border_color=(
                self.colors["border_light"],
                self.colors["border_dark"],
            ),
        )

        card.pack(
            fill="x",
            padx=8,
            pady=5,
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # ICON
        # -----------------------------------------------------

        icon_box = ctk.CTkFrame(
            card,
            width=60,
            height=60,
            corner_radius=15,
            fg_color=icon_bg,
        )

        icon_box.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 12),
            pady=14,
        )

        icon_box.grid_propagate(
            False,
        )

        icon = (
            achievement.get(
                "icon",
                "🏆",
            )
            if unlocked
            else "🔒"
        )

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Segoe UI", 27),
            text_color=icon_color,
        ).pack(
            expand=True,
        )

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------

        ctk.CTkLabel(
            card,
            text=achievement.get(
                "name",
                "Achievement",
            ),
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=3,
            pady=(16, 2),
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        ctk.CTkLabel(
            card,
            text=achievement.get(
                "description",
                "",
            ),
            font=("Segoe UI", 10),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
            anchor="w",
            wraplength=650,
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=3,
            pady=(0, 16),
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        status_text = (
            "✓  UNLOCKED"
            if unlocked
            else "🔒  LOCKED"
        )

        status = ctk.CTkLabel(
            card,
            text=status_text,
            font=("Segoe UI", 9, "bold"),
            corner_radius=8,
            fg_color=status_bg,
            text_color=status_color,
            padx=9,
            pady=5,
        )

        status.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(12, 17),
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_page(self):

        check_achievements()

        self.build_profile_contents()

        self.build_achievements()