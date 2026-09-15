import os
import json
from datetime import date

from core.task_manager import (
    load_tasks,
    get_streak,
    load_study_data
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

GAMIFICATION_FILE = os.path.join(
    DATA_DIR,
    "gamification.json"
)


DEFAULT_DATA = {
    "xp": 0,
    "completed_task_ids": [],
    "completed_sessions": 0,
    "unlocked_achievements": []
}


def ensure_file():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        GAMIFICATION_FILE
    ):

        save_gamification(
            DEFAULT_DATA.copy()
        )


def load_gamification():

    ensure_file()

    try:

        with open(
            GAMIFICATION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(
            data,
            dict
        ):
            data = {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        data = {}

    data.setdefault(
        "xp",
        0
    )

    data.setdefault(
        "completed_task_ids",
        []
    )

    data.setdefault(
        "completed_sessions",
        0
    )

    data.setdefault(
        "unlocked_achievements",
        []
    )

    save_gamification(
        data
    )

    return data


def save_gamification(data):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        GAMIFICATION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def get_level(xp=None):

    if xp is None:

        data = load_gamification()

        xp = data.get(
            "xp",
            0
        )

    # Every 500 XP = one level.
    return (int(xp) // 500) + 1


def get_level_progress(xp=None):

    if xp is None:

        data = load_gamification()

        xp = data.get(
            "xp",
            0
        )

    xp = int(xp)

    current_level_xp = (
        (xp // 500) * 500
    )

    next_level_xp = (
        current_level_xp + 500
    )

    progress_xp = (
        xp - current_level_xp
    )

    percentage = round(
        (
            progress_xp
            / 500
        ) * 100
    )

    return {
        "current_level_xp": current_level_xp,
        "next_level_xp": next_level_xp,
        "progress_xp": progress_xp,
        "percentage": percentage
    }


def calculate_task_xp(task):

    xp = 25

    priority = task.get(
        "priority",
        "Medium"
    )

    difficulty = task.get(
        "difficulty",
        "Medium"
    )

    if priority == "High":
        xp += 20

    elif priority == "Medium":
        xp += 10

    if difficulty == "Hard":
        xp += 25

    elif difficulty == "Medium":
        xp += 10

    estimated_minutes = int(
        task.get(
            "estimated_minutes",
            30
        )
    )

    if estimated_minutes >= 120:
        xp += 30

    elif estimated_minutes >= 60:
        xp += 20

    elif estimated_minutes >= 30:
        xp += 10

    return xp


def award_task_xp(task):

    data = load_gamification()

    task_id = task.get(
        "id"
    )

    if not task_id:
        return 0

    if task_id in data[
        "completed_task_ids"
    ]:

        return 0

    xp = calculate_task_xp(
        task
    )

    data["xp"] += xp

    data[
        "completed_task_ids"
    ].append(
        task_id
    )

    save_gamification(
        data
    )

    return xp


def award_session_xp():

    data = load_gamification()

    data["completed_sessions"] += 1

    # 20 XP per completed Pomodoro.
    xp = 20

    data["xp"] += xp

    save_gamification(
        data
    )

    return xp


def get_achievement_definitions():

    return [

        {
            "id": "first_task",
            "name": "First Step",
            "description": "Complete your first task.",
            "icon": "🎯"
        },

        {
            "id": "five_tasks",
            "name": "Getting Serious",
            "description": "Complete 5 tasks.",
            "icon": "🔥"
        },

        {
            "id": "twenty_tasks",
            "name": "Task Crusher",
            "description": "Complete 20 tasks.",
            "icon": "⚡"
        },

        {
            "id": "streak_3",
            "name": "3-Day Streak",
            "description": "Maintain a 3-day study streak.",
            "icon": "📚"
        },

        {
            "id": "streak_7",
            "name": "Week Warrior",
            "description": "Maintain a 7-day study streak.",
            "icon": "🏆"
        },

        {
            "id": "five_sessions",
            "name": "Focused Mind",
            "description": "Complete 5 focus sessions.",
            "icon": "🧠"
        },

        {
            "id": "twenty_sessions",
            "name": "Deep Work",
            "description": "Complete 20 focus sessions.",
            "icon": "🚀"
        },

        {
            "id": "level_5",
            "name": "Rising Scholar",
            "description": "Reach level 5.",
            "icon": "⭐"
        },

        {
            "id": "level_10",
            "name": "Study Legend",
            "description": "Reach level 10.",
            "icon": "👑"
        }
    ]


def check_achievements():

    data = load_gamification()

    tasks = load_tasks()

    completed_tasks = sum(
        1
        for task in tasks
        if task.get(
            "completed",
            False
        )
    )

    sessions = data.get(
        "completed_sessions",
        0
    )

    streak = get_streak()

    level = get_level(
        data.get(
            "xp",
            0
        )
    )

    unlocked = set(
        data.get(
            "unlocked_achievements",
            []
        )
    )

    newly_unlocked = []

    rules = {

        "first_task":
            completed_tasks >= 1,

        "five_tasks":
            completed_tasks >= 5,

        "twenty_tasks":
            completed_tasks >= 20,

        "streak_3":
            streak >= 3,

        "streak_7":
            streak >= 7,

        "five_sessions":
            sessions >= 5,

        "twenty_sessions":
            sessions >= 20,

        "level_5":
            level >= 5,

        "level_10":
            level >= 10
    }

    for achievement_id, unlocked_now in rules.items():

        if (
            unlocked_now
            and achievement_id not in unlocked
        ):

            unlocked.add(
                achievement_id
            )

            newly_unlocked.append(
                achievement_id
            )

    data[
        "unlocked_achievements"
    ] = list(
        unlocked
    )

    save_gamification(
        data
    )

    return newly_unlocked


def get_achievements():

    data = load_gamification()

    unlocked = set(
        data.get(
            "unlocked_achievements",
            []
        )
    )

    achievements = []

    for achievement in get_achievement_definitions():

        item = achievement.copy()

        item["unlocked"] = (
            item["id"] in unlocked
        )

        achievements.append(
            item
        )

    return achievements


def get_gamification_summary():

    data = load_gamification()

    xp = int(
        data.get(
            "xp",
            0
        )
    )

    level = get_level(
        xp
    )

    progress = get_level_progress(
        xp
    )

    achievements = get_achievements()

    unlocked_count = sum(
        1
        for achievement in achievements
        if achievement["unlocked"]
    )

    return {

        "xp": xp,

        "level": level,

        "progress_xp": progress[
            "progress_xp"
        ],

        "next_level_xp": progress[
            "next_level_xp"
        ],

        "percentage": progress[
            "percentage"
        ],

        "sessions": data.get(
            "completed_sessions",
            0
        ),

        "achievements": unlocked_count,

        "total_achievements": len(
            achievements
        )
    }