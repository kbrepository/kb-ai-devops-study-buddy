# Amazon Bedrock Cost and Usage Guide

## Understanding Bedrock Pricing

Amazon Bedrock pricing is primarily based on:

* Input Tokens
* Output Tokens
* Selected Foundation Model

Cost varies by model provider and model type.

---

## Current Project Usage

Current AI Features:

1. AI Interview Question Generator
2. AI Answer Evaluation
3. AI Study Plan Generator

Each feature sends prompts to Amazon Bedrock and receives generated responses.

---

## Usage Monitoring

The project includes:

### usage.json

Stores:

* Request count
* Model used
* Estimated input tokens
* Estimated output tokens

### Bedrock Usage Dashboard

Displays:

* Total Requests
* Estimated Input Tokens
* Estimated Output Tokens
* Usage History

---

## Cost Control Recommendations

### Create AWS Budget

AWS Console

Billing
→ Budgets
→ Create Budget

Recommended Learning Budget:

```text
$3 - $5 per month
```

---

### Use Smaller Models

Recommended:

* Amazon Nova Lite
* Amazon Nova Micro

Avoid larger models during experimentation.

---

### Keep Prompts Focused

Good:

```text
Generate 5 Terraform interview questions.
```

Avoid:

```text
Analyze 100 pages of documentation.
```

---

### Monitor Usage Frequently

Review:

* Bedrock Usage Dashboard
* AWS Cost Explorer
* AWS Billing Dashboard

---

## Future Improvements

* Real Token Tracking
* Daily Usage Reports
* Cost Forecasting
* Budget Alerts
* Model Comparison Dashboard

---

## Disclaimer

Token estimates within the project are approximations and should not be considered official AWS billing measurements.

Always refer to AWS Billing and Cost Explorer for actual charges.
