# Architecture

## Overview

KB AI DevOps Study Buddy is an AI-powered learning and interview preparation assistant built using Python, Streamlit, and Amazon Bedrock.

The application helps users:

* Generate study plans
* Generate interview questions
* Evaluate interview answers
* Track learning progress
* Track weak topics
* Generate learning paths
* Monitor Bedrock usage

---

## High Level Architecture

User
↓
Streamlit UI
↓
Application Layer
├── planner.py
├── interviewer.py
├── evaluator.py
├── roadmap.py
├── memory.py
├── evaluation_history.py
├── usage_tracker.py
└── bedrock_client.py
↓
Storage Layer
├── progress.json
├── evaluations.json
└── usage.json
↓
Amazon Bedrock

---

## Module Description

### planner.py

Responsible for generating study plans.

### interviewer.py

Generates interview questions using predefined question banks.

### evaluator.py

Provides rule-based answer evaluation using keyword matching.

### roadmap.py

Generates learning paths based on weak topics.

### memory.py

Stores:

* Completed topics
* Weak topics
* Study sessions

### evaluation_history.py

Stores AI evaluation history for future review.

### usage_tracker.py

Tracks Amazon Bedrock usage and estimated token consumption.

### bedrock_client.py

Handles communication with Amazon Bedrock using the Converse API.

---

## Storage Layer

### progress.json

Stores user learning progress.

### evaluations.json

Stores AI evaluation results.

### usage.json

Stores Bedrock usage statistics.

---

## Future Enhancements

* Retrieval Augmented Generation (RAG)
* PDF Upload Support
* Resume-Based Interview Questions
* EKS Troubleshooting Coach
* Personalized Learning Analytics
* Cloud Cost Estimation Dashboard
