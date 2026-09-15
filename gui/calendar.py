import customtkinter as ctk
from datetime import date
import calendar

from core.task_manager import load_tasks


class CalendarView(ctk.CTkFrame):

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

        today = date.today()

        self.year = today.year
        self.month = today.month

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.build()

    # ========================================================
    # BUILD
    # ========================================================

    def build(self):

        self.create_header()

        self.create_calendar()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#172554"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="📅 Study Calendar",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=18
        )

        self.month_label = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 18, "bold"),
            text_color="#bfdbfe"
        )

        self.month_label.grid(
            row=0,
            column=1
        )

        navigation = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        navigation.grid(
            row=0,
            column=2,
            padx=15
        )

        ctk.CTkButton(
            navigation,
            text="◀",
            width=45,
            height=35,
            command=self.previous_month
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            navigation,
            text="Today",
            width=70,
            height=35,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.go_today
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            navigation,
            text="▶",
            width=45,
            height=35,
            command=self.next_month
        ).pack(
            side="left",
            padx=4
        )

    # ========================================================
    # CALENDAR
    # ========================================================

    def create_calendar(self):

        self.calendar_frame = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color="#1e293b"
        )

        self.calendar_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        self.calendar_frame.grid_columnconfigure(
            tuple(range(7)),
            weight=1
        )

        self.calendar_frame.grid_rowconfigure(
            tuple(range(7)),
            weight=1
        )

        self.refresh_calendar()

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_calendar(self):

        for widget in (
            self.calendar_frame.winfo_children()
        ):

            widget.destroy()

        self.calendar_frame.grid_columnconfigure(
            tuple(range(7)),
            weight=1
        )

        for row in range(7):

            self.calendar_frame.grid_rowconfigure(
                row,
                weight=1
            )

        month_name = calendar.month_name[
            self.month
        ]

        self.month_label.configure(
            text=f"{month_name} {self.year}"
        )

        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        for column, day_name in enumerate(
            weekdays
        ):

            ctk.CTkLabel(
                self.calendar_frame,
                text=day_name[:3],
                font=("Arial", 12, "bold"),
                text_color="#94a3b8"
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=5,
                pady=5
            )

        tasks = load_tasks()

        weeks = calendar.monthcalendar(
            self.year,
            self.month
        )

        for row_index, week in enumerate(
            weeks,
            start=1
        ):

            for column_index, day_number in enumerate(
                week
            ):

                if day_number == 0:
                    continue

                current_date = date(
                    self.year,
                    self.month,
                    day_number
                )

                iso_date = (
                    current_date.isoformat()
                )

                day_tasks = [
                    task
                    for task in tasks
                    if task.get(
                        "due_date",
                        ""
                    ) == iso_date
                ]

                is_today = (
                    current_date == date.today()
                )

                if is_today:

                    bg = "#1d4ed8"

                elif day_tasks:

                    bg = "#14532d"

                else:

                    bg = "#263449"

                cell = ctk.CTkFrame(
                    self.calendar_frame,
                    corner_radius=12,
                    fg_color=bg
                )

                cell.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )

                ctk.CTkLabel(
                    cell,
                    text=str(day_number),
                    font=("Arial", 15, "bold"),
                    text_color="#f8fafc"
                ).pack(
                    anchor="nw",
                    padx=10,
                    pady=(8, 3)
                )

                if is_today:

                    ctk.CTkLabel(
                        cell,
                        text="TODAY",
                        font=("Arial", 9, "bold"),
                        text_color="#bfdbfe"
                    ).pack(
                        anchor="w",
                        padx=10
                    )

                if day_tasks:

                    count = len(
                        day_tasks
                    )

                    ctk.CTkLabel(
                        cell,
                        text=(
                            f"📚 {count} task"
                            if count == 1
                            else f"📚 {count} tasks"
                        ),
                        font=("Arial", 10),
                        text_color="#bbf7d0"
                    ).pack(
                        anchor="w",
                        padx=10,
                        pady=(3, 0)
                    )

                    # Show up to 2 task names.
                    for task in day_tasks[:2]:

                        ctk.CTkLabel(
                            cell,
                            text=(
                                "• "
                                + str(
                                    task.get(
                                        "task",
                                        ""
                                    )
                                )[:24]
                            ),
                            font=("Arial", 9),
                            text_color="#cbd5e1",
                            anchor="w"
                        ).pack(
                            fill="x",
                            padx=10,
                            pady=1
                        )

                    if len(day_tasks) > 2:

                        ctk.CTkLabel(
                            cell,
                            text=(
                                f"+ {len(day_tasks) - 2} more"
                            ),
                            font=("Arial", 9, "bold"),
                            text_color="#93c5fd"
                        ).pack(
                            anchor="w",
                            padx=10,
                            pady=(2, 5)
                        )

    # ========================================================
    # MONTH NAVIGATION
    # ========================================================

    def previous_month(self):

        self.month -= 1

        if self.month < 1:

            self.month = 12
            self.year -= 1

        self.refresh_calendar()

    def next_month(self):

        self.month += 1

        if self.month > 12:

            self.month = 1
            self.year += 1

        self.refresh_calendar()

    def go_today(self):

        today = date.today()

        self.year = today.year
        self.month = today.month

        self.refresh_calendar()