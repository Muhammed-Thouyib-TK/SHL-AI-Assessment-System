from app.services.retriever import retrieve_assessments


REQUIRED_FIELDS = [
    "role",
    "experience",
    "job_type"
]


def extract_information(messages):

    combined_text = " ".join(
        [message.content.lower() for message in messages]
    )

    info = {
        "role": None,
        "experience": None,
        "job_type": None
    }

    # ROLE DETECTION
    if "python" in combined_text:
        info["role"] = "Python Developer"

    elif "java" in combined_text:
        info["role"] = "Java Developer"

    elif "data scientist" in combined_text:
        info["role"] = "Data Scientist"

    elif "backend" in combined_text:
        info["role"] = "Backend Developer"

    # EXPERIENCE DETECTION
    if "entry" in combined_text or "junior" in combined_text:
        info["experience"] = "Entry Level"

    elif "mid" in combined_text:
        info["experience"] = "Mid Level"

    elif "senior" in combined_text:
        info["experience"] = "Senior Level"

    # JOB TYPE DETECTION
    if "remote" in combined_text:
        info["job_type"] = "Remote"

    elif "onsite" in combined_text:
        info["job_type"] = "Onsite"

    return info


def get_missing_field(info):

    for field in REQUIRED_FIELDS:

        if info[field] is None:
            return field

    return None


def generate_question(field):

    questions = {
        "role": "What role are you hiring for?",
        "experience": "What experience level do you need?",
        "job_type": "Is this remote or onsite?"
    }

    return questions[field]


def process_conversation(messages):

    info = extract_information(messages)

    missing_field = get_missing_field(info)

    # ASK NEXT QUESTION
    if missing_field:

        return {
            "reply": generate_question(missing_field),
            "recommendations": [],
            "end_of_conversation": False
        }

    # FINAL SEARCH QUERY
    final_query = (
        f"{info['role']} "
        f"{info['experience']} "
        f"{info['job_type']}"
    )

    # GET RECOMMENDATIONS
    recommendations = retrieve_assessments(final_query)

    return {
        "reply": "Here are the best SHL assessments for your hiring needs.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }