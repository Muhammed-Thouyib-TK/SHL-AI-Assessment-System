import re


def extract_information(messages):

    # =========================
    # COMBINE CONVERSATION
    # =========================

    combined_text = " ".join(
        [msg.content.lower() for msg in messages]
    )

    # =========================
    # INFO OBJECT
    # =========================

    info = {
        "role": None,
        "experience": None,
        "job_type": None,
        "skills": [],
        "assessment_types": [],
        "traits": [],
        "stakeholder_facing": False,
        "remote_work": False
    }

    # =========================
    # EXPERIENCE DETECTION
    # =========================

    experience_keywords = {

        "graduate": "junior",
        "fresher": "junior",
        "entry level": "junior",
        "junior": "junior",

        "mid-level": "mid-level",
        "mid level": "mid-level",

        "senior": "senior",
        "lead": "senior",
        "director": "senior",
        "experienced": "senior"
    }

    for keyword, mapped_value in experience_keywords.items():

        if keyword in combined_text:

            info["experience"] = mapped_value
            break

    # =========================
    # YEARS EXPERIENCE DETECTION
    # =========================

    years_match = re.search(
        r"(\d+)\+?\s*(years|year)",
        combined_text
    )

    if years_match and not info["experience"]:

        years = int(years_match.group(1))

        if years <= 2:
            info["experience"] = "junior"

        elif years <= 5:
            info["experience"] = "mid-level"

        else:
            info["experience"] = "senior"

    # =========================
    # JOB TYPE DETECTION
    # =========================

    job_type_keywords = [
        "remote",
        "hybrid",
        "onsite",
        "full-time",
        "part-time",
        "contract"
    ]

    for keyword in job_type_keywords:

        if keyword in combined_text:

            info["job_type"] = keyword

            if keyword == "remote":
                info["remote_work"] = True

            break

    # =========================
    # ROLE DETECTION
    # =========================

    role_patterns = [

        # Backend / Software

        "python backend developer",
        "python developer",
        "backend developer",
        "backend engineer",
        "software engineer",
        "software developer",
        "full stack developer",
        "frontend developer",
        "java developer",
        "devops engineer",
        "cloud engineer",
        "qa engineer",

        # Data

        "data analyst",
        "data scientist",
        "business analyst",

        # Business / Management

        "project manager",
        "product manager",
        "sales manager",
        "marketing manager",
        "hr manager",

        # Support

        "customer support",
        "customer support executive",

        # Design

        "ui ux designer",

        # Leadership / Consulting

        "technical consultant",
        "technical lead",
        "consultant",
        "team lead",
        "engineering manager"
    ]

    for pattern in role_patterns:

        if pattern in combined_text:

            info["role"] = pattern
            break

    # =========================
    # SMART ROLE INFERENCE
    # =========================

    if not info["role"]:

        # DATA ROLES

        if (
            "sql" in combined_text
            or "excel" in combined_text
            or "analytics" in combined_text
            or "reporting" in combined_text
            or "dashboard" in combined_text
            or "data" in combined_text
        ):

            info["role"] = "data analyst"

        # TECHNICAL ROLES

        elif (
            "python" in combined_text
            or "backend" in combined_text
            or "api" in combined_text
            or "aws" in combined_text
            or "coding" in combined_text
            or "programming" in combined_text
        ):

            info["role"] = "backend developer"

        # LEADERSHIP ROLES

        elif (
            "leadership" in combined_text
            or "stakeholder" in combined_text
            or "management" in combined_text
        ):

            info["role"] = "manager"

        # CONSULTING ROLES

        elif (
            "consultant" in combined_text
            or "client-facing" in combined_text
        ):

            info["role"] = "technical consultant"

        # SUPPORT ROLES

        elif (
            "support" in combined_text
            or "customer" in combined_text
        ):

            info["role"] = "customer support"

    # =========================
    # SKILL DETECTION
    # =========================

    skill_keywords = [

        # Programming

        "python",
        "java",
        "javascript",
        "react",
        "node",
        "sql",

        # Backend

        "apis",
        "api",
        "database",

        # Data

        "excel",
        "analytics",
        "reporting",
        "dashboard",

        # Cloud

        "aws",
        "azure",
        "cloud",
        "docker",
        "kubernetes",

        # Coding

        "coding",
        "programming",
        "development",

        # Soft skills

        "communication",
        "leadership",
        "stakeholder management",
        "problem solving",
        "critical thinking",
        "teamwork",
        "client handling"
    ]

    for skill in skill_keywords:

        if skill in combined_text:
            info["skills"].append(skill)

    info["skills"] = list(set(info["skills"]))

    # =========================
    # ASSESSMENT TYPE DETECTION
    # =========================

    assessment_type_keywords = {

        "coding": [
            "coding",
            "technical",
            "programming",
            "backend",
            "developer",
            "software",
            "python",
            "java",
            "sql"
        ],

        "personality": [
            "personality",
            "behavioral",
            "behavioural",
            "culture fit",
            "communication"
        ],

        "aptitude": [
            "aptitude",
            "cognitive",
            "reasoning",
            "analytical"
        ],

        "leadership": [
            "leadership",
            "managerial",
            "management"
        ]
    }

    for assessment_type, keywords in assessment_type_keywords.items():

        for keyword in keywords:

            if keyword in combined_text:

                info["assessment_types"].append(
                    assessment_type
                )

                break

    info["assessment_types"] = list(
        set(info["assessment_types"])
    )

    # =========================
    # TRAIT DETECTION
    # =========================

    trait_keywords = [
        "communication",
        "teamwork",
        "problem solving",
        "critical thinking",
        "leadership",
        "collaboration",
        "adaptability",
        "time management"
    ]

    for trait in trait_keywords:

        if trait in combined_text:
            info["traits"].append(trait)

    info["traits"] = list(set(info["traits"]))

    # =========================
    # STAKEHOLDER DETECTION
    # =========================

    stakeholder_keywords = [
        "stakeholder",
        "client-facing",
        "client facing",
        "consulting",
        "presentation"
    ]

    for keyword in stakeholder_keywords:

        if keyword in combined_text:

            info["stakeholder_facing"] = True
            break

    return info


def get_missing_field(info):

    if not info["role"]:
        return "role"

    if not info["experience"]:
        return "experience"

    return None


def generate_question(field):

    questions = {

        "role": (
            "What role are you hiring for?"
        ),

        "experience": (
            "What experience level do you need?"
        ),

        "job_type": (
            "Is this remote, hybrid, or onsite?"
        )
    }

    return questions.get(
        field,
        "Could you provide more details?"
    )