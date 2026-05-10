from fastapi import FastAPI
from app.models import ChatRequest, ChatResponse, Recommendation
from app.services.retriever import retrieve_assessments

from app.services.conversation import (
    extract_information,
    get_missing_field,
    generate_question
)

from app.services.retriever import retrieve_assessments

app = FastAPI()


@app.get("/")
def home():
    return {"message": "SHL AI Assignment API Running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    info = extract_information(request.messages)

    missing_field = get_missing_field(info)

    # ASK FOLLOW-UP QUESTION
    if missing_field:

        question = generate_question(missing_field)

        return ChatResponse(
            reply=question,
            recommendations=[],
            end_of_conversation=False
        )

    # BUILD SEARCH QUERY
    search_query = (
    f"{info['role']} "
    f"{info['experience']} "
    f"{info['job_type']} "
    f"python backend developer coding programming technical assessment "
    f"software engineering API databases problem solving"
)
    recommendations = retrieve_assessments(search_query)
    top_assessment = recommendations[0]["name"] if recommendations else "No assessment found"

    if not recommendations:
        return ChatResponse(
            reply="Sorry, I couldn't find suitable SHL assessments for your requirements.",
            recommendations=[],
            end_of_conversation=True
        )

    return ChatResponse(
        reply=f"I found {len(recommendations)} matching SHL assessments. Top recommendation: {top_assessment}.",
        recommendations=recommendations,
        end_of_conversation=True
    )