import json
from datetime import datetime
from pathlib import Path


EVALUATION_FILE = Path("data/evaluations.json")


def load_evaluations():
    if not EVALUATION_FILE.exists():
        return []

    with open(EVALUATION_FILE, "r") as file:
        return json.load(file)


def save_evaluations(evaluations):
    with open(EVALUATION_FILE, "w") as file:
        json.dump(evaluations, file, indent=4)


def save_ai_evaluation(topic, difficulty, question, user_answer, ai_feedback):
    evaluations = load_evaluations()

    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "difficulty": difficulty,
        "question": question,
        "user_answer": user_answer,
        "ai_feedback": ai_feedback,
    }

    evaluations.append(record)
    save_evaluations(evaluations)


def get_evaluation_history():
    return load_evaluations()