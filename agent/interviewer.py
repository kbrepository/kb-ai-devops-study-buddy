QUESTION_BANK = {
    "terraform": [
        "What is Terraform state and why is it important?",
        "What is the difference between terraform plan and terraform apply?",
        "How do you handle Terraform state locking?",
    ],
    "kubernetes": [
        "What happens when a Kubernetes Pod restarts?",
        "Difference between readiness and liveness probes?",
        "What is the role of kube-scheduler?",
    ],
    "aws": [
        "What is the difference between Security Group and NACL?",
        "How does S3 lifecycle policy work?",
        "How do you troubleshoot high CPU on EC2?",
    ],
}


def get_interview_questions(topic):
    topic = topic.lower()

    if topic in QUESTION_BANK:
        return QUESTION_BANK[topic]

    return [
        f"Explain {topic} in simple terms.",
        f"What are common production issues related to {topic}?",
        f"How would you troubleshoot {topic} in a real project?",
    ]