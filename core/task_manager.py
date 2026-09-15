import os
import json
import uuid
import calendar as calendar_module

from datetime import datetime, date, timedelta


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

TASKS_FILE = os.path.join(
    DATA_DIR,
    "tasks.json"
)

STUDY_DATA_FILE = os.path.join(
    DATA_DIR,
    "study_data.json"
)


# ============================================================
# DEFAULT TASK STRUCTURE
# ============================================================

DEFAULT_TASK = {
    "id": "",
    "task": "",
    "subject": "",
    "description": "",
    "priority": "Medium",
    "category": "Study",
    "difficulty": "Medium",
    "estimated_minutes": 30,
    "due_date": "",
    "recurring": "None",
    "completed": False,
    "starred": False,
    "completed_on": "",
    "subtasks": []
}


# ============================================================
# DATA DIRECTORY
# ============================================================

def ensure_data_directory():
    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )


# ============================================================
# STUDY DATA
# ============================================================

def ensure_study_data():
    ensure_data_directory()

    if not os.path.exists(STUDY_DATA_FILE):

        data = {
            "study_dates": [],
            "daily_goal": 5,
            "pomodoro_sessions": {},
            "total_focus_minutes": 0
        }

        save_study_data(data)

        return data

    try:

        with open(
            STUDY_DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            data = {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        data = {}

    # Add missing fields without destroying
    # existing saved information.

    data.setdefault(
        "study_dates",
        []
    )

    data.setdefault(
        "daily_goal",
        5
    )

    data.setdefault(
        "pomodoro_sessions",
        {}
    )

    data.setdefault(
        "total_focus_minutes",
        0
    )

    save_study_data(data)

    return data


def load_study_data():
    return ensure_study_data()


def save_study_data(data):
    ensure_data_directory()

    with open(
        STUDY_DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# SUBTASKS
# ============================================================

def normalize_subtasks(subtasks):

    if not isinstance(
        subtasks,
        list
    ):
        return []

    result = []

    for item in subtasks:

        # Older format:
        # ["Learn class", "Practice questions"]

        if isinstance(
            item,
            str
        ):

            text = item.strip()

            if text:

                result.append({
                    "id": str(uuid.uuid4()),
                    "text": text,
                    "completed": False
                })

        # New format:
        # {"id": "...", "text": "...", "completed": False}

        elif isinstance(
            item,
            dict
        ):

            text = str(
                item.get(
                    "text",
                    ""
                )
            ).strip()

            if text:

                result.append({
                    "id": item.get(
                        "id"
                    ) or str(uuid.uuid4()),

                    "text": text,

                    "completed": bool(
                        item.get(
                            "completed",
                            False
                        )
                    )
                })

    return result


# ============================================================
# TASK NORMALIZATION
# ============================================================

def normalize_task(task):

    normalized = DEFAULT_TASK.copy()

    if isinstance(
        task,
        dict
    ):
        normalized.update(task)

    # ID
    normalized["id"] = (
        normalized.get("id")
        or str(uuid.uuid4())
    )

    # Text fields
    normalized["task"] = str(
        normalized.get(
            "task",
            ""
        )
    ).strip()

    normalized["subject"] = str(
        normalized.get(
            "subject",
            ""
        )
    ).strip()

    normalized["description"] = str(
        normalized.get(
            "description",
            ""
        )
    ).strip()

    # Choice fields
    normalized["priority"] = (
        normalized.get(
            "priority"
        )
        or "Medium"
    )

    normalized["category"] = (
        normalized.get(
            "category"
        )
        or "Study"
    )

    normalized["difficulty"] = (
        normalized.get(
            "difficulty"
        )
        or "Medium"
    )

    normalized["recurring"] = (
        normalized.get(
            "recurring"
        )
        or "None"
    )

    # Date
    normalized["due_date"] = str(
        normalized.get(
            "due_date",
            ""
        )
    ).strip()

    # Boolean fields
    normalized["completed"] = bool(
        normalized.get(
            "completed",
            False
        )
    )

    normalized["starred"] = bool(
        normalized.get(
            "starred",
            False
        )
    )

    normalized["completed_on"] = str(
        normalized.get(
            "completed_on",
            ""
        )
    )

    # Estimated study time
    try:

        normalized["estimated_minutes"] = max(
            1,
            int(
                normalized.get(
                    "estimated_minutes",
                    30
                )
            )
        )

    except (
        ValueError,
        TypeError
    ):

        normalized["estimated_minutes"] = 30

    # Subtasks
    normalized["subtasks"] = normalize_subtasks(
        normalized.get(
            "subtasks",
            []
        )
    )

    return normalized


# ============================================================
# TASK FILE
# ============================================================

def load_tasks():

    ensure_data_directory()

    if not os.path.exists(
        TASKS_FILE
    ):

        save_tasks([])

        return []

    try:

        with open(
            TASKS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            tasks = json.load(file)

        if not isinstance(
            tasks,
            list
        ):
            tasks = []

    except (
        json.JSONDecodeError,
        OSError
    ):

        tasks = []

    normalized_tasks = [
        normalize_task(task)
        for task in tasks
    ]

    # Save normalized structure.
    save_tasks(normalized_tasks)

    return normalized_tasks


def save_tasks(tasks):

    ensure_data_directory()

    normalized_tasks = [
        normalize_task(task)
        for task in tasks
    ]

    with open(
        TASKS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            normalized_tasks,
            file,
            indent=4
        )


# ============================================================
# GET ONE TASK
# ============================================================

def get_task(task_id):

    tasks = load_tasks()

    for task in tasks:

        if task.get("id") == task_id:
            return task

    return None


# ============================================================
# DUE STATUS
# ============================================================

def get_due_status(task):

    # Completed always takes priority.
    if task.get("completed"):
        return "Completed"

    due_date = str(
        task.get(
            "due_date",
            ""
        )
    ).strip()

    if not due_date:
        return "No Due Date"

    try:

        due = datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return "No Due Date"

    today = date.today()

    if due < today:
        return "Overdue"

    if due == today:
        return "Due Today"

    return "Upcoming"


# ============================================================
# TASK PROGRESS
# ============================================================

def get_task_progress(task):

    subtasks = task.get(
        "subtasks",
        []
    )

    if subtasks:

        total = len(
            subtasks
        )

        completed = sum(
            1
            for subtask in subtasks
            if subtask.get(
                "completed",
                False
            )
        )

        return round(
            (completed / total) * 100
        )

    return (
        100
        if task.get("completed")
        else 0
    )


# ============================================================
# ADD TASK
# ============================================================

def add_task(
    task_name,
    subject="",
    priority="Medium",
    category="Study",
    difficulty="Medium",
    estimated_minutes=30,
    due_date="",
    recurring="None",
    description="",
    subtasks=None
):

    tasks = load_tasks()

    formatted_subtasks = []

    if subtasks:

        for item in subtasks:

            # Accept strings
            if isinstance(
                item,
                str
            ):

                text = item.strip()

                if text:

                    formatted_subtasks.append({
                        "id": str(uuid.uuid4()),
                        "text": text,
                        "completed": False
                    })

            # Also accept dictionaries
            elif isinstance(
                item,
                dict
            ):

                text = str(
                    item.get(
                        "text",
                        ""
                    )
                ).strip()

                if text:

                    formatted_subtasks.append({
                        "id": item.get(
                            "id"
                        ) or str(uuid.uuid4()),

                        "text": text,

                        "completed": bool(
                            item.get(
                                "completed",
                                False
                            )
                        )
                    })

    new_task = normalize_task({

        "id": str(
            uuid.uuid4()
        ),

        "task": task_name,

        "subject": subject,

        "description": description,

        "priority": priority,

        "category": category,

        "difficulty": difficulty,

        "estimated_minutes": estimated_minutes,

        "due_date": due_date,

        "recurring": recurring,

        "completed": False,

        "starred": False,

        "completed_on": "",

        "subtasks": formatted_subtasks
    })

    tasks.append(
        new_task
    )

    save_tasks(
        tasks
    )

    return new_task


# ============================================================
# UPDATE TASK
# ============================================================

def update_task(
    task_id,
    **updates
):

    tasks = load_tasks()

    updated_task = None

    for index, task in enumerate(tasks):

        if task.get("id") != task_id:
            continue

        old_completed = bool(
            task.get(
                "completed",
                False
            )
        )

        # Keep the task ID safe.
        updates.pop(
            "id",
            None
        )

        task.update(
            updates
        )

        # Normalize subtasks.
        task["subtasks"] = normalize_subtasks(
            task.get(
                "subtasks",
                []
            )
        )

        task = normalize_task(
            task
        )

        # Completion date
        if (
            task["completed"]
            and not old_completed
        ):

            task["completed_on"] = (
                date.today().isoformat()
            )

        elif not task["completed"]:

            task["completed_on"] = ""

        tasks[index] = task

        updated_task = task

        break

    save_tasks(
        tasks
    )

    return updated_task


# ============================================================
# TOGGLE TASK COMPLETION
# ============================================================

def toggle_completion(task_id):

    tasks = load_tasks()

    target_task = None
    was_completed = False

    for task in tasks:

        if task.get("id") != task_id:
            continue

        target_task = task

        was_completed = bool(
            task.get(
                "completed",
                False
            )
        )

        task["completed"] = not was_completed

        if task["completed"]:

            task["completed_on"] = (
                date.today().isoformat()
            )

            # Completing the whole task
            # completes all subtasks.
            for subtask in task.get(
                "subtasks",
                []
            ):

                subtask["completed"] = True

        else:

            task["completed_on"] = ""

            # Undo the task:
            # reset subtasks too.
            for subtask in task.get(
                "subtasks",
                []
            ):

                subtask["completed"] = False

        break

    save_tasks(
        tasks
    )

    # Create next recurring occurrence
    # after a pending task becomes completed.
    if (
        target_task
        and not was_completed
        and target_task.get(
            "recurring",
            "None"
        ) != "None"
    ):

        create_next_recurring_task(
            target_task
        )

    return target_task


# ============================================================
# TOGGLE SUBTASK
# ============================================================

def toggle_subtask(
    task_id,
    subtask_id
):

    tasks = load_tasks()

    result = None

    for task in tasks:

        if task.get("id") != task_id:
            continue

        for subtask in task.get(
            "subtasks",
            []
        ):

            if subtask.get("id") != subtask_id:
                continue

            subtask["completed"] = not bool(
                subtask.get(
                    "completed",
                    False
                )
            )

            progress = get_task_progress(
                task
            )

            # All subtasks complete
            if (
                task.get("subtasks")
                and progress == 100
            ):

                task["completed"] = True

                task["completed_on"] = (
                    date.today().isoformat()
                )

            # At least one subtask unfinished
            else:

                task["completed"] = False

                task["completed_on"] = ""

            result = task

            break

        break

    save_tasks(
        tasks
    )

    return result


# ============================================================
# STAR / IMPORTANT TASK
# ============================================================

def toggle_star(task_id):

    tasks = load_tasks()

    result = None

    for task in tasks:

        if task.get("id") == task_id:

            task["starred"] = not bool(
                task.get(
                    "starred",
                    False
                )
            )

            result = task

            break

    save_tasks(
        tasks
    )

    return result


# ============================================================
# DELETE TASK
# ============================================================

def delete_task(task_id):

    tasks = load_tasks()

    new_tasks = [
        task
        for task in tasks
        if task.get("id") != task_id
    ]

    save_tasks(
        new_tasks
    )

    return len(
        tasks
    ) != len(
        new_tasks
    )


# ============================================================
# SEARCH
# ============================================================

def search_tasks(query):

    tasks = load_tasks()

    query = str(
        query or ""
    ).lower().strip()

    if not query:
        return tasks

    results = []

    for task in tasks:

        searchable_text = " ".join([
            str(
                task.get(
                    "task",
                    ""
                )
            ),

            str(
                task.get(
                    "subject",
                    ""
                )
            ),

            str(
                task.get(
                    "description",
                    ""
                )
            ),

            str(
                task.get(
                    "category",
                    ""
                )
            ),

            str(
                task.get(
                    "difficulty",
                    ""
                )
            )
        ]).lower()

        if query in searchable_text:

            results.append(
                task
            )

    return results


# ============================================================
# FILTER TASKS
# ============================================================

def filter_tasks(
    tasks,
    priority="All",
    status="All",
    category="All",
    difficulty="All",
    starred=False
):

    filtered = []

    for task in tasks:

        if (
            priority != "All"
            and task.get(
                "priority"
            ) != priority
        ):
            continue

        if (
            status != "All"
            and get_due_status(
                task
            ) != status
        ):
            continue

        if (
            category != "All"
            and task.get(
                "category"
            ) != category
        ):
            continue

        if (
            difficulty != "All"
            and task.get(
                "difficulty"
            ) != difficulty
        ):
            continue

        if (
            starred
            and not task.get(
                "starred",
                False
            )
        ):
            continue

        filtered.append(
            task
        )

    return filtered


# ============================================================
# SORT TASKS
# ============================================================

def sort_tasks(
    tasks,
    sort_by="Default"
):

    if sort_by == "Priority":

        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2
        }

        return sorted(
            tasks,
            key=lambda task: (
                priority_order.get(
                    task.get(
                        "priority",
                        "Medium"
                    ),
                    99
                ),

                task.get(
                    "due_date"
                ) or "9999-12-31"
            )
        )

    if sort_by == "Due Date":

        return sorted(
            tasks,
            key=lambda task: (
                task.get(
                    "due_date"
                ) or "9999-12-31"
            )
        )

    if sort_by == "Study Time":

        return sorted(
            tasks,
            key=lambda task: int(
                task.get(
                    "estimated_minutes",
                    30
                )
            ),
            reverse=True
        )

    if sort_by == "Difficulty":

        difficulty_order = {
            "Hard": 0,
            "Medium": 1,
            "Easy": 2
        }

        return sorted(
            tasks,
            key=lambda task: difficulty_order.get(
                task.get(
                    "difficulty",
                    "Medium"
                ),
                99
            )
        )

    if sort_by == "Progress":

        return sorted(
            tasks,
            key=lambda task: get_task_progress(
                task
            ),
            reverse=True
        )

    if sort_by == "Name":

        return sorted(
            tasks,
            key=lambda task: str(
                task.get(
                    "task",
                    ""
                )
            ).lower()
        )

    return tasks


# ============================================================
# RECURRING TASK SUPPORT
# ============================================================

def get_next_recurring_date(
    current_date,
    recurring
):

    if recurring == "Daily":

        return (
            current_date
            + timedelta(days=1)
        )

    if recurring == "Weekly":

        return (
            current_date
            + timedelta(days=7)
        )

    if recurring == "Monthly":

        year = current_date.year

        month = (
            current_date.month
            + 1
        )

        if month > 12:

            month = 1

            year += 1

        max_day = calendar_module.monthrange(
            year,
            month
        )[1]

        day = min(
            current_date.day,
            max_day
        )

        return date(
            year,
            month,
            day
        )

    return None


def create_next_recurring_task(
    task
):

    recurring = task.get(
        "recurring",
        "None"
    )

    if recurring == "None":
        return None

    current_due = str(
        task.get(
            "due_date",
            ""
        )
    ).strip()

    if current_due:

        try:

            current_date = datetime.strptime(
                current_due,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            current_date = date.today()

    else:

        current_date = date.today()

    next_date = get_next_recurring_date(
        current_date,
        recurring
    )

    if next_date is None:
        return None

    tasks = load_tasks()

    new_subtasks = []

    for subtask in task.get(
        "subtasks",
        []
    ):

        new_subtasks.append({

            "id": str(
                uuid.uuid4()
            ),

            "text": subtask.get(
                "text",
                ""
            ),

            "completed": False
        })

    next_task = normalize_task({

        "id": str(
            uuid.uuid4()
        ),

        "task": task.get(
            "task",
            ""
        ),

        "subject": task.get(
            "subject",
            ""
        ),

        "description": task.get(
            "description",
            ""
        ),

        "priority": task.get(
            "priority",
            "Medium"
        ),

        "category": task.get(
            "category",
            "Study"
        ),

        "difficulty": task.get(
            "difficulty",
            "Medium"
        ),

        "estimated_minutes": task.get(
            "estimated_minutes",
            30
        ),

        "due_date": next_date.isoformat(),

        "recurring": recurring,

        "completed": False,

        "starred": task.get(
            "starred",
            False
        ),

        "completed_on": "",

        "subtasks": new_subtasks
    })

    tasks.append(
        next_task
    )

    save_tasks(
        tasks
    )

    return next_task


# ============================================================
# TODAY'S TASKS
# ============================================================

def get_today_tasks():

    tasks = load_tasks()

    today = date.today().isoformat()

    return [
        task
        for task in tasks
        if (
            task.get(
                "due_date"
            ) == today
            and not task.get(
                "completed"
            )
        )
    ]


# ============================================================
# UPCOMING TASKS
# ============================================================

def get_upcoming_tasks(
    days=7
):

    tasks = load_tasks()

    today = date.today()

    last_day = (
        today
        + timedelta(days=days)
    )

    results = []

    for task in tasks:

        if task.get("completed"):
            continue

        due_date = task.get(
            "due_date",
            ""
        )

        if not due_date:
            continue

        try:

            due = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        if (
            today
            <= due
            <= last_day
        ):

            results.append(
                task
            )

    return sorted(
        results,
        key=lambda task: (
            task.get(
                "due_date"
            ) or "9999-12-31"
        )
    )


# ============================================================
# OVERDUE TASKS
# ============================================================

def get_overdue_tasks():

    tasks = load_tasks()

    return [
        task
        for task in tasks
        if get_due_status(
            task
        ) == "Overdue"
    ]


# ============================================================
# IMPORTANT / STARRED TASKS
# ============================================================

def get_starred_tasks():

    tasks = load_tasks()

    return [
        task
        for task in tasks
        if task.get(
            "starred",
            False
        )
    ]


# ============================================================
# COMPLETED TASKS
# ============================================================

def get_completed_tasks():

    tasks = load_tasks()

    return [
        task
        for task in tasks
        if task.get(
            "completed",
            False
        )
    ]


# ============================================================
# PENDING TASKS
# ============================================================

def get_pending_tasks():

    tasks = load_tasks()

    return [
        task
        for task in tasks
        if not task.get(
            "completed",
            False
        )
    ]


# ============================================================
# SUBJECT PROGRESS
# ============================================================

def get_subject_progress():

    tasks = load_tasks()

    subjects = {}

    for task in tasks:

        subject = (
            task.get(
                "subject"
            )
            or "General"
        )

        if subject not in subjects:

            subjects[subject] = {
                "total": 0,
                "completed": 0,
                "progress": 0,
                "minutes": 0
            }

        subjects[subject]["total"] += 1

        subjects[subject]["minutes"] += int(
            task.get(
                "estimated_minutes",
                30
            )
        )

        if task.get("completed"):

            subjects[subject]["completed"] += 1

    for subject in subjects:

        total = subjects[subject]["total"]

        completed = subjects[subject]["completed"]

        subjects[subject]["progress"] = (
            round(
                (completed / total) * 100
            )
            if total
            else 0
        )

    return subjects


# ============================================================
# CATEGORY STATISTICS
# ============================================================

def get_category_statistics():

    tasks = load_tasks()

    categories = {}

    for task in tasks:

        category = task.get(
            "category",
            "Study"
        )

        if category not in categories:

            categories[category] = {
                "total": 0,
                "completed": 0,
                "minutes": 0
            }

        categories[category]["total"] += 1

        categories[category]["minutes"] += int(
            task.get(
                "estimated_minutes",
                30
            )
        )

        if task.get("completed"):

            categories[category]["completed"] += 1

    return categories


# ============================================================
# STATISTICS
# ============================================================

def get_statistics(tasks=None):
    """
    Supports both:

        get_statistics()

    and:

        get_statistics(tasks)

    This keeps older Dashboard code compatible.
    """

    if tasks is None:
        tasks = load_tasks()

    # Ensure everything has the new structure.
    tasks = [
        normalize_task(task)
        for task in tasks
    ]

    total = len(
        tasks
    )

    completed = sum(
        1
        for task in tasks
        if task.get(
            "completed",
            False
        )
    )

    pending = (
        total
        - completed
    )

    overdue = sum(
        1
        for task in tasks
        if get_due_status(
            task
        ) == "Overdue"
    )

    today_count = sum(
        1
        for task in tasks
        if get_due_status(
            task
        ) == "Due Today"
    )

    estimated_minutes = sum(
        int(
            task.get(
                "estimated_minutes",
                30
            )
        )
        for task in tasks
        if not task.get(
            "completed",
            False
        )
    )

    total_progress = sum(
        get_task_progress(task)
        for task in tasks
    )

    average_progress = (
        round(
            total_progress / total
        )
        if total
        else 0
    )

    completion_percentage = (
        round(
            (completed / total)
            * 100
        )
        if total
        else 0
    )

    # Total estimated minutes for all tasks
    total_planned_minutes = sum(
        int(
            task.get(
                "estimated_minutes",
                30
            )
        )
        for task in tasks
    )

    # Completed estimated time
    completed_minutes = sum(
        int(
            task.get(
                "estimated_minutes",
                30
            )
        )
        for task in tasks
        if task.get(
            "completed",
            False
        )
    )

    return {

        "total": total,

        "completed": completed,

        "pending": pending,

        "overdue": overdue,

        "today": today_count,

        "progress": completion_percentage,

        "average_progress": average_progress,

        "estimated_minutes": estimated_minutes,

        "total_planned_minutes": total_planned_minutes,

        "completed_minutes": completed_minutes
    }


# ============================================================
# DAILY GOAL PROGRESS
# ============================================================

def get_daily_goal_progress():

    data = load_study_data()

    goal = max(
        1,
        int(
            data.get(
                "daily_goal",
                5
            )
        )
    )

    today = date.today().isoformat()

    tasks = load_tasks()

    completed_today = 0

    for task in tasks:

        if (
            task.get(
                "completed"
            )
            and task.get(
                "completed_on"
            ) == today
        ):

            completed_today += 1

    percentage = min(
        100,
        round(
            (
                completed_today
                / goal
            )
            * 100
        )
    )

    return {
        "goal": goal,
        "completed": completed_today,
        "percentage": percentage
    }


# ============================================================
# POMODORO RECORDING
# ============================================================

def record_focus_session(
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
        return

    if minutes <= 0:
        return

    data = load_study_data()

    today = date.today().isoformat()

    sessions = data.setdefault(
        "pomodoro_sessions",
        {}
    )

    sessions[today] = (
        sessions.get(
            today,
            0
        )
        + 1
    )

    data["total_focus_minutes"] = (
        data.get(
            "total_focus_minutes",
            0
        )
        + minutes
    )

    study_dates = data.setdefault(
        "study_dates",
        []
    )

    if today not in study_dates:

        study_dates.append(
            today
        )

    save_study_data(
        data
    )


# ============================================================
# TODAY'S FOCUS STATISTICS
# ============================================================

def get_today_focus_stats():

    data = load_study_data()

    today = date.today().isoformat()

    sessions = data.get(
        "pomodoro_sessions",
        {}
    )

    return {
        "sessions": sessions.get(
            today,
            0
        ),

        "minutes": (
            sessions.get(
                today,
                0
            )
            * 25
        )
    }


# ============================================================
# STREAK
# ============================================================

def get_streak():

    data = load_study_data()

    study_dates = set(
        data.get(
            "study_dates",
            []
        )
    )

    if not study_dates:
        return 0

    current = date.today()

    streak = 0

    while current.isoformat() in study_dates:

        streak += 1

        current -= timedelta(
            days=1
        )

    return streak