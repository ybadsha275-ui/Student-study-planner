import os
import json
from datetime import datetime


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

STUDY_FILE = os.path.join(
    DATA_DIR,
    "study_data.json"
)

GAMIFICATION_FILE = os.path.join(
    DATA_DIR,
    "gamification.json"
)


def read_json(path):

    if not os.path.exists(path):
        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def write_json(
    path,
    data
):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def create_backup(
    output_path
):

    backup = {

        "application": "Student Study Planner",

        "backup_date":
            datetime.now().isoformat(),

        "tasks":
            read_json(
                TASKS_FILE
            ),

        "study_data":
            read_json(
                STUDY_FILE
            ),

        "gamification":
            read_json(
                GAMIFICATION_FILE
            )
    }

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            backup,
            file,
            indent=4
        )

    return output_path


def restore_backup(
    backup_path
):

    with open(
        backup_path,
        "r",
        encoding="utf-8"
    ) as file:

        backup = json.load(
            file
        )

    if not isinstance(
        backup,
        dict
    ):
        raise ValueError(
            "Invalid backup format."
        )

    if "tasks" not in backup:
        raise ValueError(
            "Backup does not contain task data."
        )

    write_json(
        TASKS_FILE,
        backup.get(
            "tasks",
            []
        )
    )

    write_json(
        STUDY_FILE,
        backup.get(
            "study_data",
            {}
        )
    )

    write_json(
        GAMIFICATION_FILE,
        backup.get(
            "gamification",
            {}
        )
    )

    return True