# SHL Assessment Recommendation System

An AI-powered conversational recommendation system that suggests relevant SHL assessments based on hiring requirements.

## Features

- Conversational hiring assistant
- Multi-turn interaction
- Semantic search using Sentence Transformers
- SHL catalog recommendation engine
- FastAPI backend
- Intelligent ranking and filtering

## Tech Stack

- Python
- FastAPI
- SentenceTransformers
- Scikit-learn
- JSON dataset

## Project Structure

app/
├── main.py
├── models.py
├── services/
│   ├── conversation.py
│   ├── retriever.py
│   └── llm_service.py
├── data/
│   └── shl_catalog.json

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example Query

- Need Python backend developer assessment
- Mid-level
- Remote

## Output

Returns ranked SHL assessment recommendations with:
- assessment name
- URL
- assessment type
- similarity score

## Future Improvements

- LLM integration
- Better reranking
- Web frontend
- User authentication
- Deployment on cloud