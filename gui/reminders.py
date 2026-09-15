import customtkinter as ctk
from datetime import date, datetime, timedelta

from core.task_manager import (
    load_tasks,
    get_due_status
)


class ReminderManager:

    CHECK_INTERVAL = 60 * 1000  # 1 minute

    def __init__(self, app):

        self.app = app
        self.enabled = True
        self.after_id = None

        self.start()

    # =========================================================
    # START REMINDER SYSTEM
    # =========================================================

    def start(self):
        self.check_reminders()

    # =========================================================
    # CHECK REMINDERS
    # =========================================================

    def check_reminders(self):

        if not self.enabled:
            self.schedule_next_check()
            return

        try:

            tasks = load_tasks()

            today = date.today()

            overdue = []
            due_today = []
            tomorrow = []

            for task in tasks:

                if task.get("completed"):
                    continue

                status = get_due_status(task)

                if status == "Overdue":
                    overdue.append(task)

                elif status == "Due Today":
                    due_today.append(task)

                else:

                    due_date = task.get(
                        "due_date",
                        ""
                    )

                    if due_date:

                        try:

                            due = datetime.strptime(
                                due_date,
                                "%Y-%m-%d"
                            ).date()

                            if due == today + timedelta(days=1):
                                tomorrow.append(task)

                        except ValueError:
                            pass

            # Show the most important reminder first.
            if overdue:

                self.show_reminder(
                    "Overdue Tasks",
                    self.build_message(
                        "You have overdue tasks:",
                        overdue
                    )
                )

            elif due_today:

                self.show_reminder(
                    "Tasks Due Today",
                    self.build_message(
                        "These tasks are due today:",
                        due_today
                    )
                )

            elif tomorrow:

                self.show_reminder(
                    "Tomorrow's Deadlines",
                    self.build_message(
                        "You have deadlines tomorrow:",
                        tomorrow
                    )
                )

        except Exception:
            # A reminder error should never crash
            # the whole application.
            pass

        self.schedule_next_check()

    # =========================================================
    # SCHEDULE NEXT CHECK
    # =========================================================

    def schedule_next_check(self):

        try:

            self.after_id = self.app.after(
                self.CHECK_INTERVAL,
                self.check_reminders
            )

        except Exception:
            self.after_id = None

    # =========================================================
    # BUILD MESSAGE
    # =========================================================

    def build_message(
        self,
        heading,
        tasks
    ):

        lines = [
            heading,
            ""
        ]

        for task in tasks[:5]:

            task_name = task.get(
                "task",
                "Untitled Task"
            )

            priority = task.get(
                "priority",
                "Medium"
            )

            lines.append(
                f"• {task_name} ({priority})"
            )

        if len(tasks) > 5:

            lines.append(
                f"\n+ {len(tasks) - 5} more task(s)"
            )

        return "\n".join(lines)

    # =========================================================
    # SHOW REMINDER
    # =========================================================

    def show_reminder(
        self,
        title,
        message
    ):

        # Don't open multiple reminder windows
        # at the same time.

        if getattr(
            self.app,
            "_reminder_visible",
            False
        ):
            return

        self.app._reminder_visible = True

        reminder = ctk.CTkToplevel(
            self.app
        )

        reminder.title(
            title
        )

        reminder.geometry(
            "410x270"
        )

        reminder.resizable(
            False,
            False
        )

        reminder.transient(
            self.app
        )

        reminder.grab_set()

        # -----------------------------------------------------
        # Position bottom-right of application
        # -----------------------------------------------------

        self.app.update_idletasks()

        x = (
            self.app.winfo_x()
            + self.app.winfo_width()
            - 430
        )

        y = (
            self.app.winfo_y()
            + self.app.winfo_height()
            - 320
        )

        reminder.geometry(
            f"410x270+{max(x, 0)}+{max(y, 0)}"
        )

        # -----------------------------------------------------
        # Main card
        # -----------------------------------------------------

        card = ctk.CTkFrame(
            reminder,
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
            text="🔔",
            font=("Segoe UI", 28)
        ).pack(
            pady=(15, 2)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 19, "bold")
        ).pack(
            pady=2
        )

        ctk.CTkLabel(
            card,
            text=message,
            justify="left",
            anchor="w",
            wraplength=350,
            font=("Segoe UI", 11)
        ).pack(
            fill="x",
            padx=20,
            pady=10
        )

        def close():

            self.app._reminder_visible = False

            try:
                reminder.grab_release()
            except Exception:
                pass

            try:
                reminder.destroy()
            except Exception:
                pass

        ctk.CTkButton(
            card,
            text="Got it",
            width=120,
            command=close
        ).pack(
            pady=(0, 15)
        )

        reminder.protocol(
            "WM_DELETE_WINDOW",
            close
        )

    # =========================================================
    # ENABLE / DISABLE
    # =========================================================

    def set_enabled(
        self,
        enabled
    ):

        self.enabled = bool(
            enabled
        )

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        if self.after_id is not None:

            try:
                self.app.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

            self.after_id = None