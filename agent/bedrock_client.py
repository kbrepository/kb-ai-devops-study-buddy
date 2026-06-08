import os
import boto3
from dotenv import load_dotenv


load_dotenv()


def generate_ai_interview_questions(topic, difficulty, count):
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")

    client = boto3.client("bedrock-runtime", region_name=region)

    prompt = f"""
You are a DevOps interview coach/expert.

Generate {count} interview questions for this topic:
Topic: {topic}
Difficulty: {difficulty}

Focus on AWS, Terraform, Kubernetes, CI/CD, Linux, and real-world troubleshooting.
Along with that focus on other technologies related to DevOps as well.

Return only numbered questions.
"""

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={
            "maxTokens": 500,
            "temperature": 0.7,
        },
    )

    return response["output"]["message"]["content"][0]["text"]