# Amazon Bedrock Setup Guide

## Prerequisites

* AWS Account
* AWS CLI Installed
* Python 3.x
* Amazon Bedrock Access Enabled

---

## Configure AWS CLI

Verify installation:

```bash
aws --version
```

Configure credentials:

```bash
aws configure
```

Provide:

* AWS Access Key
* AWS Secret Access Key
* Region
* Output Format

Example:

```text
Region: us-east-1
Output: json
```

---

## Enable Bedrock Model Access

AWS Console

Amazon Bedrock
→ Model Access
→ Manage Model Access

Enable desired models.

Recommended for learning:

* Amazon Nova Lite
* Amazon Nova Micro
* Claude Haiku

---

## Environment Variables

Create:

```bash
touch .env
```

Example:

```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

---

## Install Dependencies

```bash
pip install boto3 python-dotenv
```

---

## Verify Bedrock Access

Run the application and test:

* AI Interview Question Generator
* AI Answer Evaluation
* AI Study Plan Generator

---

## Security Notes

Never commit:

* .env
* AWS credentials
* Access keys

Ensure .gitignore contains:

```text
.env
venv/
__pycache__/
```
