import boto3
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_embedding(text):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION")
    )

    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": text
        })
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]