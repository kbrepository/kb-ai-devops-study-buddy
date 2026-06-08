LEARNING_PATHS = {
    "terraform state": [
        "Terraform State",
        "Remote Backend",
        "State Locking",
        "State Drift",
        "Import Existing Resources",
    ],
    "kubernetes probes": [
        "Pod Lifecycle",
        "Readiness Probe",
        "Liveness Probe",
        "Startup Probe",
        "Troubleshooting Failed Pods",
    ],
    "iam": [
        "IAM Users",
        "IAM Roles",
        "IAM Policies",
        "Permission Boundaries",
        "Cross Account Access",
    ],
}
from agent.memory import load_progress


def generate_learning_path():
    progress = load_progress()

    weak_topics = progress.get("weak_topics", [])

    if not weak_topics:
        return ["Terraform State"]

    learning_path = []

    for topic in weak_topics:
        topic_lower = topic.lower()

        if topic_lower in LEARNING_PATHS:
            learning_path.extend(
                LEARNING_PATHS[topic_lower]
            )
        else:
            learning_path.append(topic)

    learning_path = list(dict.fromkeys(learning_path))
    return learning_path