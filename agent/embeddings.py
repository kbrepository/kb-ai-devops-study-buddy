import boto3
import json
import os

from botocore.config import Config
from dotenv import load_dotenv


load_dotenv()


BEDROCK_CONFIG = Config(
    connect_timeout=5,
    read_timeout=30,
    retries={
        "max_attempts": 5,
        "mode": "adaptive",
    },
)


def get_embedding(text):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        config=BEDROCK_CONFIG,
    )

    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": text
        }),
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]