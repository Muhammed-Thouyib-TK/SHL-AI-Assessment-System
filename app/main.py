from fastapi import FastAPI

from app.models import ChatRequest, ChatResponse

from app.services.retriever import retrieve_assessments

from app.services.conversation import (
    extract_information,
    get_missing_field,
    generate_question
)

from app.services.llm_service import generate_reply

from app.utils.helpers import (
    is_off_topic,
    is_prompt_injection
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "SHL AI Assignment API Running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # =========================
    # TURN LIMIT PROTECTION
    # =========================

    if len(request.messages) >= 8:

        return ChatResponse(
            reply=(
                "Based on the provided conversation, "
                "I recommend reviewing the shortlisted "
                "SHL assessments above."
            ),
            recommendations=[],
            end_of_conversation=True
        )

    latest_message = request.messages[-1].content.lower()

    # =========================
    # PROMPT INJECTION PROTECTION
    # =========================

    if is_prompt_injection(latest_message):

        return ChatResponse(
            reply=(
                "I can only provide SHL assessment "
                "recommendations from the official catalog."
            ),
            recommendations=[],
            end_of_conversation=True
        )

    # =========================
    # OFF-TOPIC REFUSAL
    # =========================

    if is_off_topic(latest_message):

        return ChatResponse(
            reply=(
                "I can only help with SHL assessment "
                "recommendations and catalog-related queries."
            ),
            recommendations=[],
            end_of_conversation=True
        )

    # =========================
    # EXTRACT CONVERSATION INFO
    # =========================

    info = extract_information(request.messages)

    # =========================
    # HANDLE COMPARISON QUESTIONS
    # =========================

    comparison_keywords = [
        "difference",
        "compare",
        "vs",
        "versus"
    ]

    if any(
        word in latest_message
        for word in comparison_keywords
    ):

        # =========================
        # OPQ VS GSA
        # =========================

        if (
            "opq" in latest_message
            and "gsa" in latest_message
        ):

            return ChatResponse(
                reply=(
                    "OPQ assessments focus on workplace "
                    "personality traits, behavioral style, "
                    "and interpersonal preferences. "
                    "GSA assessments focus on cognitive "
                    "abilities such as reasoning, learning "
                    "capacity, and problem-solving skills. "
                    "Organizations typically use OPQ for "
                    "behavioral fit and leadership insights, "
                    "while GSA is used to measure aptitude "
                    "and general mental ability."
                ),
                recommendations=[],
                end_of_conversation=True
            )

        # =========================
        # PERSONALITY VS APTITUDE
        # =========================

        if (
            "personality" in latest_message
            and "aptitude" in latest_message
        ):

            return ChatResponse(
                reply=(
                    "Personality assessments measure "
                    "behavioral tendencies, communication "
                    "style, motivation, and workplace fit. "
                    "Aptitude assessments measure cognitive "
                    "skills such as reasoning, numerical "
                    "ability, problem-solving, and learning "
                    "potential. SHL personality tests are "
                    "commonly used for leadership and team "
                    "fit, while aptitude tests support "
                    "technical and analytical hiring."
                ),
                recommendations=[],
                end_of_conversation=True
            )

        # =========================
        # GENERAL COMPARISON
        # =========================

        return ChatResponse(
            reply=(
                "SHL assessment comparisons are typically "
                "based on assessment type, competencies "
                "measured, duration, adaptive capability, "
                "and intended hiring use case. Please "
                "mention the specific assessments you "
                "would like to compare."
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # =========================
    # HANDLE VERY VAGUE QUERIES
    # =========================

    if len(latest_message.split()) < 3:

        return ChatResponse(
            reply=(
                "Could you provide more details about "
                "the role, required skills, or "
                "experience level?"
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # =========================
    # SMART EXPERIENCE DETECTION
    # =========================

    graduate_keywords = [
        "graduate",
        "fresher",
        "entry level",
        "junior",
        "intern"
    ]

    if not info["experience"]:

        if any(
            word in latest_message
            for word in graduate_keywords
        ):

            info["experience"] = (
                "graduate entry level"
            )

    # =========================
    # ASK FOLLOW-UP QUESTIONS
    # =========================

    missing_field = get_missing_field(info)

    if missing_field:

        if (
            missing_field == "experience"
            and info["experience"]
        ):

            missing_field = None

    if missing_field:

        question = generate_question(
            missing_field
        )

        return ChatResponse(
            reply=question,
            recommendations=[],
            end_of_conversation=False
        )

    # =========================
    # BUILD SEARCH QUERY
    # =========================

    query_parts = []

    if info["role"]:
        query_parts.append(info["role"])

    if info["experience"]:
        query_parts.append(info["experience"])

    if info["job_type"]:
        query_parts.append(info["job_type"])

    if info["skills"]:
        query_parts.extend(info["skills"])

    if info["assessment_types"]:
        query_parts.extend(
            info["assessment_types"]
        )

    if info["traits"]:
        query_parts.extend(info["traits"])

    if info["stakeholder_facing"]:

        query_parts.append(
            "stakeholder communication leadership"
        )

    if info["remote_work"]:

        query_parts.append(
            "remote collaboration adaptability"
        )

    # =========================
    # GRADUATE BIAS
    # =========================

    if (
        "graduate" in latest_message
        or "junior" in latest_message
        or "entry level" in latest_message
    ):

        query_parts.extend([
            "entry level",
            "graduate aptitude",
            "numerical reasoning",
            "analytical skills"
        ])

    # =========================
    # SQL / EXCEL BIAS
    # =========================

    if "sql" in latest_message:

        query_parts.extend([
            "sql",
            "data analysis",
            "analytical reasoning"
        ])

    if "excel" in latest_message:

        query_parts.extend([
            "excel",
            "data interpretation",
            "numerical ability"
        ])

    # =========================
    # PYTHON BIAS
    # =========================

    if "python" in latest_message:

        query_parts.extend([
            "python coding",
            "backend development",
            "programming"
        ])

    # =========================
    # AWS BIAS
    # =========================

    if "aws" in latest_message:

        query_parts.extend([
            "cloud",
            "aws",
            "technical skills"
        ])

    # =========================
    # COMMUNICATION BIAS
    # =========================

    if "communication" in latest_message:

        query_parts.extend([
            "communication",
            "stakeholder interaction",
            "collaboration"
        ])

    # =========================
    # LEADERSHIP BIAS
    # =========================

    if "leadership" in latest_message:

        query_parts.extend([
            "leadership",
            "management",
            "decision making"
        ])

    # =========================
    # ALWAYS INCLUDE CONTEXT
    # =========================

    query_parts.extend([
        "assessment",
        "hiring",
        "evaluation"
    ])

    search_query = " ".join(query_parts)

    # =========================
    # RETRIEVE ASSESSMENTS
    # =========================

    recommendations = retrieve_assessments(
        search_query
    )

    # =========================
    # NO RESULTS
    # =========================

    if not recommendations:

        return ChatResponse(
            reply=(
                "Sorry, I couldn't find suitable "
                "SHL assessments for your "
                "requirements."
            ),
            recommendations=[],
            end_of_conversation=True
        )

    # =========================
    # GENERATE LLM RESPONSE
    # =========================

    llm_reply = generate_reply(
        user_message=search_query,
        recommendations=recommendations
    )

    return ChatResponse(
        reply=llm_reply,
        recommendations=recommendations[:10],
        end_of_conversation=True
    )