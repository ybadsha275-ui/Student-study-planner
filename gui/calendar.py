import customtkinter as ctk

from datetime import date
import calendar

from core.task_manager import load_tasks


class CalendarView(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        app,
    ):

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
        # CURRENT DATE
        # =====================================================

        today = date.today()

        self.year = today.year
        self.month = today.month

        # =====================================================
        # LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            1,
            weight=1,
        )

        self.build()

    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        self.create_header()
        self.create_calendar()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = ctk.CTkFrame(
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

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 14),
        )

        header.grid_columnconfigure(
            0,
            weight=1,
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=16,
        )

        ctk.CTkLabel(
            title_frame,
            text="STUDY SCHEDULE",
            font=("Segoe UI", 10, "bold"),
            text_color=(
                self.colors["accent"],
                "#60A5FA",
            ),
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            title_frame,
            text="Study Calendar",
            font=("Segoe UI", 25, "bold"),
        ).pack(
            anchor="w",
            pady=(2, 2),
        )

        ctk.CTkLabel(
            title_frame,
            text="View upcoming deadlines and planned study tasks.",
            font=("Segoe UI", 11),
            text_color=(
                self.colors["muted_light"],
                self.colors["muted_dark"],
            ),
        ).pack(
            anchor="w",
        )

        # -----------------------------------------------------
        # MONTH DISPLAY
        # -----------------------------------------------------

        month_frame = ctk.CTkFrame(
            header,
            corner_radius=13,
            fg_color=(
                "#F2F6FB",
                "#202B38",
            ),
        )

        month_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=13,
        )

        self.month_label = ctk.CTkLabel(
            month_frame,
            text="",
            font=("Segoe UI", 17, "bold"),
            text_color=(
                self.colors["text_light"],
                self.colors["text_dark"],
            ),
        )

        self.month_label.pack(
            padx=22,
            pady=10,
        )

        # -----------------------------------------------------
        # NAVIGATION
        # -----------------------------------------------------

        navigation = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        navigation.grid(
            row=0,
            column=2,
            padx=(5, 18),
            pady=12,
        )

        ctk.CTkButton(
            navigation,
            text="‹",
            width=38,
            height=36,
            corner_radius=10,
            font=("Segoe UI Symbol", 18, "bold"),
            fg_color=(
                "#E8EEF6",
                "#273442",
            ),
            hover_color=(
                "#DCE5F0",
                "#334252",
            ),
            text_color=(
                "#334155",
                "#E2E8F0",
            ),
            command=self.previous_month,
        ).pack(
            side="left",
            padx=3,
        )

        ctk.CTkButton(
            navigation,
            text="Today",
            width=75,
            height=36,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.go_today,
        ).pack(
            side="left",
            padx=3,
        )

        ctk.CTkButton(
            navigation,
            text="›",
            width=38,
            height=36,
            corner_radius=10,
            font=("Segoe UI Symbol", 18, "bold"),
            fg_color=(
                "#E8EEF6",
                "#273442",
            ),
            hover_color=(
                "#DCE5F0",
                "#334252",
            ),
            text_color=(
                "#334155",
                "#E2E8F0",
            ),
            command=self.next_month,
        ).pack(
            side="left",
            padx=3,
        )

    # =========================================================
    # CALENDAR
    # =========================================================

    def create_calendar(self):

        outer = ctk.CTkFrame(
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

        outer.grid(
            row=1,
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
        # LEGEND
        # -----------------------------------------------------

        legend = ctk.CTkFrame(
            outer,
            fg_color="transparent",
        )

        legend.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(14, 6),
        )

        legend.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            legend,
            text="MONTH VIEW",
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

        legend_items = ctk.CTkFrame(
            legend,
            fg_color="transparent",
        )

        legend_items.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.legend_item(
            legend_items,
            "Today",
            (
                "#DBEAFE",
                "#173252",
            ),
            (
                "#2563EB",
                "#60A5FA",
            ),
        )

        self.legend_item(
            legend_items,
            "Has Tasks",
            (
                "#DCFCE7",
                "#16372A",
            ),
            (
                "#15803D",
                "#4ADE80",
            ),
        )

        self.calendar_frame = ctk.CTkFrame(
            outer,
            corner_radius=15,
            fg_color=(
                "#F8FAFC",
                "#121921",
            ),
        )

        self.calendar_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(4, 14),
        )

        self.calendar_frame.grid_columnconfigure(
            tuple(range(7)),
            weight=1,
        )

        self.calendar_frame.grid_rowconfigure(
            tuple(range(7)),
            weight=1,
        )

        self.refresh_calendar()

    # =========================================================
    # LEGEND ITEM
    # =========================================================

    def legend_item(
        self,
        parent,
        text,
        background,
        foreground,
    ):

        item = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        item.pack(
            side="left",
            padx=(8, 0),
        )

        dot = ctk.CTkFrame(
            item,
            width=10,
            height=10,
            corner_radius=5,
            fg_color=background,
        )

        dot.pack(
            side="left",
            padx=(0, 5),
        )

        dot.pack_propagate(False)

        ctk.CTkLabel(
            item,
            text=text,
            font=("Segoe UI", 9),
            text_color=foreground,
        ).pack(
            side="left",
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_calendar(self):

        for widget in self.calendar_frame.winfo_children():

            widget.destroy()

        # -----------------------------------------------------
        # GRID
        # -----------------------------------------------------

        self.calendar_frame.grid_columnconfigure(
            tuple(range(7)),
            weight=1,
        )

        for row in range(7):

            self.calendar_frame.grid_rowconfigure(
                row,
                weight=1,
            )

        # -----------------------------------------------------
        # MONTH
        # -----------------------------------------------------

        month_name = calendar.month_name[
            self.month
        ]

        self.month_label.configure(
            text=f"{month_name} {self.year}",
        )

        # -----------------------------------------------------
        # TASK DATA
        # -----------------------------------------------------

        tasks = load_tasks()

        # -----------------------------------------------------
        # WEEKDAYS
        # -----------------------------------------------------

        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        for column, day_name in enumerate(
            weekdays
        ):

            header_cell = ctk.CTkFrame(
                self.calendar_frame,
                corner_radius=9,
                fg_color=(
                    "#EEF2F7",
                    "#1C2631",
                ),
            )

            header_cell.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=4,
                pady=4,
            )

            ctk.CTkLabel(
                header_cell,
                text=day_name[:3].upper(),
                font=("Segoe UI", 10, "bold"),
                text_color=(
                    "#526174",
                    "#9BA9B8",
                ),
            ).pack(
                expand=True,
            )

        # -----------------------------------------------------
        # MONTH WEEKS
        # -----------------------------------------------------

        weeks = calendar.monthcalendar(
            self.year,
            self.month,
        )

        for row_index, week in enumerate(
            weeks,
            start=1,
        ):

            for column_index, day_number in enumerate(
                week
            ):

                if day_number == 0:

                    empty = ctk.CTkFrame(
                        self.calendar_frame,
                        corner_radius=11,
                        fg_color="transparent",
                    )

                    empty.grid(
                        row=row_index,
                        column=column_index,
                        sticky="nsew",
                        padx=4,
                        pady=4,
                    )

                    continue

                current_date = date(
                    self.year,
                    self.month,
                    day_number,
                )

                iso_date = (
                    current_date.isoformat()
                )

                day_tasks = [
                    task
                    for task in tasks
                    if task.get(
                        "due_date",
                        "",
                    ) == iso_date
                ]

                is_today = (
                    current_date == date.today()
                )

                self.create_day_cell(
                    row_index,
                    column_index,
                    day_number,
                    day_tasks,
                    is_today,
                )

    # =========================================================
    # DAY CELL
    # =========================================================

    def create_day_cell(
        self,
        row,
        column,
        day_number,
        day_tasks,
        is_today,
    ):

        # -----------------------------------------------------
        # CELL COLORS
        # -----------------------------------------------------

        if is_today:

            background = (
                "#EAF2FF",
                "#173252",
            )

            border = (
                "#8BB8F8",
                "#3569A5",
            )

            number_color = (
                "#1D4ED8",
                "#60A5FA",
            )

        elif day_tasks:

            background = (
                "#F0FDF4",
                "#173025",
            )

            border = (
                "#BBE8C5",
                "#28593A",
            )

            number_color = (
                "#166534",
                "#4ADE80",
            )

        else:

            background = (
                "#FFFFFF",
                "#161E27",
            )

            border = (
                "#E2E8F0",
                "#27323E",
            )

            number_color = (
                "#334155",
                "#CBD5E1",
            )

        cell = ctk.CTkFrame(
            self.calendar_frame,
            corner_radius=12,
            fg_color=background,
            border_width=1,
            border_color=border,
        )

        cell.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=4,
            pady=4,
        )

        # -----------------------------------------------------
        # DAY NUMBER
        # -----------------------------------------------------

        top = ctk.CTkFrame(
            cell,
            fg_color="transparent",
        )

        top.pack(
            fill="x",
            padx=9,
            pady=(7, 2),
        )

        top.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            top,
            text=str(day_number),
            font=("Segoe UI", 15, "bold"),
            text_color=number_color,
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        if is_today:

            today_badge = ctk.CTkLabel(
                top,
                text="TODAY",
                font=("Segoe UI", 7, "bold"),
                corner_radius=5,
                fg_color=(
                    "#DBEAFE",
                    "#23466F",
                ),
                text_color=(
                    "#2563EB",
                    "#93C5FD",
                ),
                padx=5,
                pady=2,
            )

            today_badge.grid(
                row=0,
                column=1,
                sticky="e",
            )

        # -----------------------------------------------------
        # TASK COUNT
        # -----------------------------------------------------

        if day_tasks:

            count = len(
                day_tasks
            )

            count_text = (
                f"{count} task"
                if count == 1
                else f"{count} tasks"
            )

            ctk.CTkLabel(
                cell,
                text=f"📚 {count_text}",
                font=("Segoe UI", 9, "bold"),
                text_color=(
                    "#15803D",
                    "#4ADE80",
                ),
            ).pack(
                anchor="w",
                padx=9,
                pady=(1, 3),
            )

            # -------------------------------------------------
            # TASK PREVIEW
            # -------------------------------------------------

            for task in day_tasks[:2]:

                task_name = str(
                    task.get(
                        "task",
                        "",
                    )
                )

                if len(task_name) > 20:

                    task_name = (
                        task_name[:20]
                        + "…"
                    )

                ctk.CTkLabel(
                    cell,
                    text=f"• {task_name}",
                    font=("Segoe UI", 9),
                    text_color=(
                        "#475569",
                        "#C5D0DC",
                    ),
                    anchor="w",
                ).pack(
                    fill="x",
                    padx=9,
                    pady=1,
                )

            # -------------------------------------------------
            # MORE TASKS
            # -------------------------------------------------

            if len(day_tasks) > 2:

                ctk.CTkLabel(
                    cell,
                    text=(
                        f"+ {len(day_tasks) - 2} more"
                    ),
                    font=("Segoe UI", 8, "bold"),
                    text_color=(
                        "#2563EB",
                        "#60A5FA",
                    ),
                    anchor="w",
                ).pack(
                    fill="x",
                    padx=9,
                    pady=(2, 4),
                )

        else:

            ctk.CTkLabel(
                cell,
                text="No tasks",
                font=("Segoe UI", 8),
                text_color=(
                    "#94A3B8",
                    "#667586",
                ),
            ).pack(
                anchor="w",
                padx=9,
                pady=(4, 5),
            )

    # =========================================================
    # PREVIOUS MONTH
    # =========================================================

    def previous_month(self):

        self.month -= 1

        if self.month < 1:

            self.month = 12
            self.year -= 1

        self.refresh_calendar()

    # =========================================================
    # NEXT MONTH
    # =========================================================

    def next_month(self):

        self.month += 1

        if self.month > 12:

            self.month = 1
            self.year += 1

        self.refresh_calendar()

    # =========================================================
    # TODAY
    # =========================================================

    def go_today(self):

        today = date.today()

        self.year = today.year
        self.month = today.month

        self.refresh_calendar()