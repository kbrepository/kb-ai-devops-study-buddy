import os
import boto3
from dotenv import load_dotenv
from agent.usage_tracker import log_bedrock_usage


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
    output_text = response["output"]["message"]["content"][0]["text"]

    log_bedrock_usage(
        feature="AI Interview Questions",
        model_id=model_id,
        input_text=prompt,
        output_text=output_text,
    )

    return output_text

    # return response["output"]["message"]["content"][0]["text"]

def evaluate_answer_with_ai(topic, question, user_answer, difficulty):
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")

    client = boto3.client("bedrock-runtime", region_name=region)

    prompt = f"""
You are a strict but supportive DevOps interview evaluator.

Evaluate the candidate's answer.

Topic: {topic}
Difficulty: {difficulty}

Interview Question:
{question}

Candidate Answer:
{user_answer}

Return the response in this format:

Score: <score>/10

Strengths:
- point 1
- point 2

Missing Points:
- point 1
- point 2

Improved Answer:
Write a better interview-ready answer in simple language.

Next Study Suggestion:
Suggest one topic the candidate should revise next.
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
            "maxTokens": 900,
            "temperature": 0.4,
        },
    )

    output_text = response["output"]["message"]["content"][0]["text"]

    log_bedrock_usage(
        feature="AI Answer Evaluation",
        model_id=model_id,
        input_text=prompt,
        output_text=output_text,
    )

    return output_text