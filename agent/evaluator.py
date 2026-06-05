EXPECTED_KEYWORDS = {
    "terraform state": [
        "state file",
        "resource mapping",
        "remote backend",
        "state locking",
        "drift",
    ],
    "s3 lifecycle": [
        "transition",
        "expiration",
        "storage class",
        "prefix",
        "rule",
    ],
    "kubernetes probes": [
        "readiness",
        "liveness",
        "container health",
        "restart",
        "traffic",
    ],
}


def evaluate_answer(topic, user_answer):
    topic = topic.lower()
    user_answer = user_answer.lower()

    expected_keywords = EXPECTED_KEYWORDS.get(topic)

    if not expected_keywords:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "feedback": "No evaluation rule found for this topic yet.",
        }

    matched = [
        keyword for keyword in expected_keywords
        if keyword in user_answer
    ]

    missing = [
        keyword for keyword in expected_keywords
        if keyword not in user_answer
    ]

    score = int((len(matched) / len(expected_keywords)) * 10)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "feedback": "Good attempt. Review the missing points to improve your answer.",
    }