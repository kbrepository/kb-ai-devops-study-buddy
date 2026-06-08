import json
from datetime import datetime
from pathlib import Path


USAGE_FILE = Path("data/usage.json")


def estimate_tokens(text):
    if not text:
        return 0

    return max(1, len(text.split()) * 2)


def load_usage():
    if not USAGE_FILE.exists():
        return []

    with open(USAGE_FILE, "r") as file:
        return json.load(file)


def save_usage(usage_data):
    with open(USAGE_FILE, "w") as file:
        json.dump(usage_data, file, indent=4)


def log_bedrock_usage(feature, model_id, input_text, output_text):
    usage_data = load_usage()

    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feature": feature,
        "model_id": model_id,
        "estimated_input_tokens": estimate_tokens(input_text),
        "estimated_output_tokens": estimate_tokens(output_text),
    }

    usage_data.append(record)
    save_usage(usage_data)


def get_usage_summary():
    usage_data = load_usage()

    total_requests = len(usage_data)
    total_input_tokens = sum(item["estimated_input_tokens"] for item in usage_data)
    total_output_tokens = sum(item["estimated_output_tokens"] for item in usage_data)

    return {
        "total_requests": total_requests,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "records": usage_data,
    }