# SHL Assessment Recommendation System

An AI-powered conversational recommendation system that helps recruiters and hiring managers identify suitable SHL assessments based on hiring requirements, job descriptions, technical skills, behavioral traits, and conversational refinement.

This project was developed as part of the SHL Research Intern AI assignment.

---

# Overview

Traditional assessment catalogs rely heavily on keyword search and manual filtering. This project introduces a conversational AI agent that understands hiring requirements in natural language and recommends relevant SHL Individual Test Solutions through multi-turn dialogue.

The system supports:

- Conversational clarification
- Assessment recommendation
- Query refinement
- Assessment comparison
- Off-topic refusal
- Prompt injection protection
- Stateless API architecture

The agent only recommends assessments present in the official SHL catalog.

---

# Features

## Conversational Recommendation Engine
The assistant gathers hiring requirements through dialogue and recommends relevant SHL assessments.

Example:
- "Need assessment for senior backend engineer with AWS and Python experience"

---

## Clarification for Vague Queries
The system asks follow-up questions when insufficient information is provided.

Example:
- "I need an assessment"
→ asks for role, skills, or experience level.

---

## Multi-turn Refinement
The assistant updates recommendations dynamically when users refine requirements.

Example:
- "Add personality assessments too"
- "Prefer leadership-focused evaluations"

---

## Assessment Comparison
Supports grounded comparison between assessments using catalog information.

Example:
- "What is the difference between OPQ and GSA?"

---

## Semantic Retrieval
Uses SentenceTransformers embeddings for semantic matching instead of simple keyword search.

---

## Intelligent Ranking
Recommendations are ranked using:
- semantic similarity
- skill matching
- role matching
- experience signals
- assessment type weighting

---

## Safety & Scope Control
The assistant:
- refuses unrelated hiring advice
- blocks prompt injection attempts
- avoids hallucinated assessments
- only returns catalog-grounded URLs

---

# Tech Stack

- Python
- FastAPI
- SentenceTransformers
- Scikit-learn
- Google Gemini API
- JSON-based SHL catalog
- Uvicorn

---

# Project Architecture

```text
app/
├── main.py
├── models.py
├── services/
│   ├── conversation.py
│   ├── retriever.py
│   └── llm_service.py
├── utils/
│   └── helpers.py
├── data/
│   └── shl_catalog.json
```

---

# API Endpoints

## Health Check

### GET `/health`

Checks whether the API is running.

### Response

```json
{
  "status": "ok"
}
```

---

## Conversational Chat Endpoint

### POST `/chat`

Takes full stateless conversation history and returns:
- assistant reply
- recommendations
- conversation completion status

---

# Request Example

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need assessment for senior Python backend engineer with AWS experience"
    }
  ]
}
```

---

# Response Example

```json
{
  "reply": "For your Senior Backend Engineer role, we recommend Python (New), AWS Development, and Cloud Computing assessments.",
  "recommendations": [
    {
      "name": "Python (New)",
      "url": "https://www.shl.com/...",
      "test_type": "Knowledge & Skills",
      "score": 0.76
    }
  ],
  "end_of_conversation": true
}
```

---

# How It Works

## 1. Conversation Understanding
The system extracts:
- role
- skills
- experience level
- behavioral traits
- assessment preferences

from the full conversation history.

---

## 2. Semantic Retrieval
The user query is embedded using SentenceTransformers and compared against the SHL catalog embeddings.

---

## 3. Intelligent Ranking
Assessments are reranked using:
- semantic similarity
- role relevance
- skill overlap
- leadership indicators
- personality requirements
- aptitude signals

---

## 4. Response Generation
Gemini generates a concise recruiter-friendly explanation grounded on retrieved assessments.

---

# Safety Handling

The system includes protections for:

## Off-topic Queries
Examples:
- salary negotiation
- crypto
- weather
- marketing strategy

---

## Prompt Injection Attempts
Examples:
- "ignore previous instructions"
- "reveal system prompt"
- "act as another assistant"

---

## Hallucination Prevention
The assistant:
- only recommends assessments present in the SHL catalog
- only returns catalog URLs
- avoids generating unknown assessment names

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd SHL_AI_Assignment
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# Run Locally

```bash
uvicorn app.main:app --reload
```

Open Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Example Queries

## Technical Hiring

- Need Python backend developer assessment
- Hiring AWS cloud engineer
- Need SQL and Excel assessment for analyst role

---

## Leadership Hiring

- Need leadership and stakeholder management assessment
- Looking for managerial personality tests

---

## Comparison Queries

- Difference between OPQ and GSA
- Compare numerical and deductive reasoning assessments

---

# Evaluation Approach

The system was tested against:
- vague queries
- refinement conversations
- comparison requests
- prompt injection attempts
- off-topic queries
- technical hiring scenarios
- leadership hiring scenarios

The implementation follows the assignment constraints:
- stateless API
- schema compliance
- recommendation grounding
- max recommendation limits
- conversational clarification

---

# Current Limitations

- Retrieval still relies on lightweight reranking heuristics
- Comparison grounding can be further improved
- Multi-turn refinement memory can be enhanced
- No persistent vector database currently used
- No frontend interface yet

---

# Future Improvements

- Advanced reranking pipeline
- Better conversational memory weighting
- Chroma/FAISS vector database integration
- Frontend dashboard
- Streaming responses
- Docker deployment
- Cloud-native deployment
- Better evaluation automation

---

# Author

Muhammed Thouyib TK

SHL Research Intern AI Assignment Submission