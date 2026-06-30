# Project Milestones

## Project Goal

Build an AI-powered DevOps learning and interview preparation assistant using:

* Python
* Streamlit
* Amazon Bedrock
* Retrieval Augmented Generation (RAG)
* JSON-based memory and tracking

The objective is to learn AI Engineering concepts through a practical project aligned with Cloud and DevOps skills.

---

# Phase 1 – Rule-Based Agent Foundation

## Milestone 1

Basic Study Plan Generator

### Concepts Learned

* Functions
* Modular Design
* User Input Processing

### Features Added

* Generate study plans
* Topic-based learning plans

---

## Milestone 2

Interview Question Mode

### Concepts Learned

* Knowledge Representation
* Static Question Banks

### Features Added

* Generate interview questions
* Topic-specific preparation

---

## Milestone 3

Progress Memory using JSON

### Concepts Learned

* Persistent Storage
* State Management

### Features Added

* progress.json
* Study session tracking
* Weak topic storage

---

## Milestone 4

Weak Topic Recommendation Engine

### Concepts Learned

* Recommendation Logic
* Learning Feedback Loops

### Features Added

* Weak topic tracking
* Recommended next topic

---

## Milestone 5

Daily Study Plan Generator

### Concepts Learned

* Planning Systems
* Personalized Learning Paths

### Features Added

* Daily learning recommendations

---

## Milestone 6

Rule-Based Interview Evaluation Engine

### Concepts Learned

* Evaluation Logic
* Keyword-Based Assessment

### Features Added

* Answer scoring
* Missing concept detection
* Weak topic updates

---

## Milestone 7

Latest Session Summary

### Concepts Learned

* Session Analytics
* Learning Review

### Features Added

* Study session summary
* Weak topic overview

---

## Milestone 8

Learning Path Generator

### Concepts Learned

* Planning
* Goal Decomposition

### Features Added

* Personalized learning roadmap

---

# Phase 2 – User Interface

## Milestone 9

Streamlit User Interface

### Concepts Learned

* Frontend Development
* State-Aware UI Design

### Features Added

* Streamlit application
* Navigation menu
* Interactive learning dashboard

---

## Milestone 10

UI Improvements and Documentation

### Concepts Learned

* User Experience
* Documentation Practices

### Features Added

* Homepage improvements
* Project documentation structure

---

# Phase 3 – Amazon Bedrock Integration

## Milestone 11

Amazon Bedrock Integration

### Concepts Learned

* Foundation Models
* Prompt Engineering
* Converse API

### Features Added

* AI Interview Question Generator

---

## Milestone 12

Bedrock Usage Dashboard

### Concepts Learned

* AI Observability
* Cost Awareness
* Usage Tracking

### Features Added

* usage.json
* Request tracking
* Token estimation
* Usage dashboard

---

## Milestone 13

AI Answer Evaluation

### Concepts Learned

* LLM-Based Assessment
* Structured Prompt Design

### Features Added

* AI scoring
* AI feedback
* Improved answer generation
* Weak topic recommendations

---

## Milestone 14

Evaluation History

### Concepts Learned

* Historical Analysis
* Learning Progress Tracking

### Features Added

* evaluations.json
* Evaluation history dashboard

---

## Milestone 15

AI Study Plan Generator

### Concepts Learned

* Personalized Learning Systems
* Context-Aware Prompting

### Features Added

* AI-generated study plans
* Weak-topic-aware recommendations

---

# Phase 4 – Documentation and Architecture

## Milestone 16

Project Documentation

### Concepts Learned

* Technical Writing
* Project Documentation

### Features Added

* architecture.md
* milestones.md
* bedrock-setup.md
* cost-and-usage.md

---

## Milestone 17

Architecture and GitHub Improvements

### Concepts Learned

* System Design Communication

### Features Added

* README improvements
* Screenshots
* Architecture documentation

---

# Phase 5 – Retrieval Augmented Generation (RAG)

## Milestone 18

RAG V0 – Knowledge Base Assistant

### Concepts Learned

* Retrieval Augmented Generation
* Context Injection

### Features Added

* knowledge_base/
* Notes Assistant
* Markdown-based retrieval

### Key Learning

Retrieval is NOT the same as the LLM.

The retriever decides what information reaches the model.

---

## Milestone 19

RAG V1 – Retrieval Improvements

### Concepts Learned

* Text Normalization
* Chunking
* Retrieval Debugging

### Features Added

* Query normalization
* Markdown section chunking
* Source tracking
* Retrieved context visibility

### Important Discovery

A single character such as:

?
.
,
!

can affect retrieval quality.

This highlighted why production RAG systems are difficult.

---

## Milestone 20

RAG V1.1 – Keyword Scoring Retrieval

### Concepts Learned

* Lexical Search
* Search Ranking
* Relevance Scoring

### Features Added

* Keyword extraction
* Overlap scoring
* Ranked retrieval
* Top-K search

### Key Learning

Lexical Search:

Query
↓
Keyword Matching
↓
Ranked Results

Vector Search:

Query
↓
Embedding
↓
Semantic Similarity
↓
Ranked Results

---

# Upcoming Milestones

## Milestone 21
RAG V2 – Semantic Search using Titan Embeddings

### Concepts Learned
- Embeddings
- Vector Representation
- Cosine Similarity
- Semantic Retrieval
- JSON-backed Vector Store

### Features Added
- Titan Embeddings integration
- vector_store.json
- Vector store builder
- Semantic search engine
- Similarity score display

### Key Learning
Embeddings convert text into numerical meaning coordinates. Semantic search retrieves relevant chunks based on meaning, not exact keyword matches.
---

## Milestone 22
Streamlit Semantic RAG Integration

### Concepts Learned
- End-to-end RAG application flow
- Retrieved context debugging
- Context-aware answer generation

### Features Added
- AI Notes Assistant using Semantic RAG
- Retrieved chunks expander
- Similarity score visibility
- Full context sent to Bedrock

### Key Learning
A good RAG system must expose retrieved context for debugging. When answers are poor, first inspect retrieval before blaming the LLM.

## Milestone 23

RAG V3 – Vector Database

Potential Technologies:

* ChromaDB
* FAISS
* OpenSearch
* Pinecone

---

## Milestone 24

PDF Knowledge Base

Features:

* PDF Upload
* PDF Chunking
* PDF Retrieval

---

## Milestone 25

Resume-Based Interview Assistant

Features:

* Resume Analysis
* Personalized Interview Questions
* Gap Analysis

---

## Milestone 26

Deployment

Options:

* Streamlit Cloud
* EC2
* ECS Fargate
* App Runner

---

## Milestone 27

Medium Blog Series

Planned Topics:

* Building an AI DevOps Study Buddy
* What I Learned About AI Agents
* Why RAG Is Hard in Production
* Retrieval Is Not Equal To The LLM
* Lexical Search vs Vector Search
* Chunking and Context Windows
* Observability in AI Applications
* Building RAG Using Amazon Bedrock

---

# Current Project Status

Current Stage:

Phase 5 – RAG V1.1

Current Capabilities:

✓ Study Planning

✓ AI Study Planning

✓ Interview Question Generation

✓ AI Interview Question Generation

✓ Rule-Based Evaluation

✓ AI Evaluation

✓ Evaluation History

✓ Learning Paths

✓ Usage Dashboard

✓ Amazon Bedrock Integration

✓ RAG Knowledge Base

✓ Chunking

✓ Keyword Scoring Retrieval

Next Major Learning Objective:

Semantic Search and Embeddings
