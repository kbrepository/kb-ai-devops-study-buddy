import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("data/progress.json")


def load_progress():
    if not DATA_FILE.exists():
        return {
            "completed_topics": [],
            "weak_topics": [],
            "study_sessions": []
        }

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_progress(progress):
    with open(DATA_FILE, "w") as file:
        json.dump(progress, file, indent=4)


def add_study_session(topic, duration, difficulty):
    progress = load_progress()

    session = {
        "topic": topic,
        "duration": duration,
        "difficulty": difficulty,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    progress["study_sessions"].append(session)

    if topic not in progress["completed_topics"]:
        progress["completed_topics"].append(topic)

    save_progress(progress)


def add_weak_topic(topic):
    progress = load_progress()

    if topic not in progress["weak_topics"]:
        progress["weak_topics"].append(topic)

    save_progress(progress)


def view_progress():
    return load_progress()

def get_recommended_topic():
    progress = load_progress()
    weak_topics = progress.get("weak_topics", [])

    if weak_topics:
        return weak_topics[0]

    return "Terraform state"