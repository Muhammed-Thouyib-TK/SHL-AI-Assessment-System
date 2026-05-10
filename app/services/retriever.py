import json
import re

from sentence_transformers import SentenceTransformer, util


# =========================
# LOAD MODEL
# =========================

model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# LOAD CATALOG
# =========================

with open("app/data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)


# =========================
# BUILD EMBEDDINGS
# =========================

assessment_texts = []

for assessment in assessments:

    combined_text = f"""
    Name: {assessment.get('name', '')}

    Test Type: {assessment.get('test_type', '')}

    Description: {assessment.get('description', '')}

    Job Levels: {' '.join(assessment.get('job_levels', []))}

    Languages: {' '.join(assessment.get('languages', []))}

    Skills: {' '.join(assessment.get('skills', []))}

    Keywords: {' '.join(assessment.get('keys', []))}

    Duration: {assessment.get('duration', '')}

    Remote Testing: {assessment.get('remote', '')}

    Adaptive Testing: {assessment.get('adaptive', '')}
    """

    assessment_texts.append(combined_text)


assessment_embeddings = model.encode(
    assessment_texts,
    convert_to_tensor=True
)


# =========================
# HELPERS
# =========================

def contains_keywords(query, keywords):

    query = query.lower()

    return any(keyword in query for keyword in keywords)


# =========================
# KEYWORD GROUPS
# =========================

TECH_KEYWORDS = [
    "python",
    "java",
    "sql",
    "aws",
    "api",
    "backend",
    "frontend",
    "developer",
    "software",
    "coding",
    "programming",
    "cloud",
    "machine learning",
    "ai",
    "database"
]

DATA_KEYWORDS = [
    "data analyst",
    "analytics",
    "excel",
    "reporting",
    "sql",
    "data",
    "analysis",
    "business intelligence",
    "visualization"
]

LEADERSHIP_KEYWORDS = [
    "leadership",
    "management",
    "manager",
    "stakeholder",
    "executive",
    "director"
]

COMMUNICATION_KEYWORDS = [
    "communication",
    "client",
    "presentation",
    "collaboration",
    "interaction"
]


# =========================
# MAIN RETRIEVAL
# =========================

def retrieve_assessments(query, top_k=10):

    query_lower = query.lower()

    query_words = set(
        re.findall(r"\w+", query_lower)
    )

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        query_embedding,
        assessment_embeddings
    )[0]

    scored_results = []

    for idx, similarity_score in enumerate(similarities):

        assessment = assessments[idx]

        name = assessment.get("name", "")

        description = assessment.get(
            "description",
            ""
        )

        keys = " ".join(
            assessment.get("keys", [])
        )

        skills = " ".join(
            assessment.get("skills", [])
        )

        languages = " ".join(
            assessment.get("languages", [])
        )

        job_levels = " ".join(
            assessment.get("job_levels", [])
        )

        duration = assessment.get(
            "duration",
            ""
        )

        remote = assessment.get(
            "remote",
            ""
        )

        adaptive = assessment.get(
            "adaptive",
            ""
        )

        combined_text = f"""
        {name}

        {description}

        {keys}

        {skills}

        {languages}

        {job_levels}

        Duration: {duration}

        Remote Testing: {remote}

        Adaptive Testing: {adaptive}
        """.lower()

        final_score = float(similarity_score)

        # =========================
        # TECH BOOSTING
        # =========================

        if contains_keywords(
            query_lower,
            TECH_KEYWORDS
        ):

            technical_terms = [
                "python",
                "java",
                "sql",
                "coding",
                "developer",
                "programming",
                "backend",
                "api",
                "cloud",
                "aws",
                "software",
                "technical",
                "database"
            ]

            if any(
                term in combined_text
                for term in technical_terms
            ):
                final_score += 0.20

            if "personality" in combined_text:
                final_score -= 0.12

            if "leadership" in combined_text:
                final_score -= 0.08

        # =========================
        # DATA BOOSTING
        # =========================

        if contains_keywords(
            query_lower,
            DATA_KEYWORDS
        ):

            data_terms = [
                "sql",
                "analytics",
                "excel",
                "reporting",
                "data",
                "visualization",
                "business intelligence",
                "reasoning",
                "numerical",
                "deductive"
            ]

            if any(
                term in combined_text
                for term in data_terms
            ):
                final_score += 0.20

            bad_data_terms = [
                "sap",
                "abap",
                "hybris",
                "mulesoft",
                "oracle dba",
                "basis",
                "teradata",
                "ssis",
                "ssas",
                "asp.net",
                "dot net",
                "c#",
                "sharepoint"
            ]

            if any(
                term in combined_text
                for term in bad_data_terms
            ):
                final_score -= 0.45

        # =========================
        # LEADERSHIP BOOSTING
        # =========================

        if contains_keywords(
            query_lower,
            LEADERSHIP_KEYWORDS
        ):

            leadership_terms = [
                "leadership",
                "management",
                "manager",
                "executive",
                "stakeholder",
                "decision",
                "behavior"
            ]

            if any(
                term in combined_text
                for term in leadership_terms
            ):
                final_score += 0.20

            coding_terms = [
                "python",
                "java",
                "developer",
                "backend",
                "coding"
            ]

            if any(
                term in combined_text
                for term in coding_terms
            ):
                final_score -= 0.35

        # =========================
        # COMMUNICATION BOOSTING
        # =========================

        if contains_keywords(
            query_lower,
            COMMUNICATION_KEYWORDS
        ):

            communication_terms = [
                "communication",
                "presentation",
                "interaction",
                "client",
                "collaboration"
            ]

            if any(
                term in combined_text
                for term in communication_terms
            ):
                final_score += 0.15

        # =========================
        # METADATA BOOSTING
        # =========================

        metadata_boost = 0

        for level in assessment.get(
            "job_levels",
            []
        ):

            if level.lower() in query_lower:
                metadata_boost += 0.12

        if "remote" in query_lower:

            if remote == "yes":
                metadata_boost += 0.10

        if "adaptive" in query_lower:

            if adaptive == "yes":
                metadata_boost += 0.10

        if (
            "short" in query_lower
            or "quick" in query_lower
            or "fast" in query_lower
        ):

            minutes_match = re.search(
                r"(\d+)",
                duration
            )

            if minutes_match:

                mins = int(
                    minutes_match.group(1)
                )

                if mins <= 15:
                    metadata_boost += 0.10

        final_score += metadata_boost

        # =========================
        # EXACT MATCH BOOST
        # =========================

        exact_matches = 0

        for word in query_words:

            if (
                len(word) > 2
                and word in combined_text
            ):
                exact_matches += 1

        final_score += exact_matches * 0.03

        # =========================
        # SAVE RESULT
        # =========================

        scored_results.append({
            "name": name,
            "url": assessment.get("link", ""),
            "test_type": ", ".join(
                assessment.get("keys", [])
            ),
            "remote_support": remote,
            "adaptive_support": adaptive,
            "duration": duration,
            "score": round(final_score, 2)
        })

    # =========================
    # SORT RESULTS
    # =========================

    scored_results = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    # =========================
    # REMOVE NOISY RESULTS
    # =========================

    blocked_keywords = [
        "sample report",
        "participant report",
        "manager report sample",
        "profile report sample"
    ]

    filtered_results = []

    for result in scored_results:

        name_lower = result["name"].lower()

        if any(
            keyword in name_lower
            for keyword in blocked_keywords
        ):
            continue

        # =========================
        # PYTHON CLEANUP
        # =========================

        if "python" in query_lower:

            bad_python = [
                "ruby",
                "php",
                "javascript",
                "sap",
                "mulesoft",
                "oracle"
            ]

            if any(
                bad in name_lower
                for bad in bad_python
            ):
                continue

        # =========================
        # DATA ANALYST CLEANUP
        # =========================

        if (
            "data analyst" in query_lower
            or "sql" in query_lower
            or "excel" in query_lower
        ):

            bad_data = [
                "sap",
                "abap",
                "hybris",
                "mulesoft",
                "basis",
                "teradata",
                "ssis",
                "ssas",
                "asp.net",
                "dot net",
                "sharepoint"
            ]

            if any(
                bad in name_lower
                for bad in bad_data
            ):
                continue

        # =========================
        # LEADERSHIP CLEANUP
        # =========================

        if (
            "leadership" in query_lower
            or "management" in query_lower
        ):

            bad_leadership = [
                "python",
                "java",
                "developer",
                "backend",
                "coding"
            ]

            if any(
                bad in name_lower
                for bad in bad_leadership
            ):
                continue

        # =========================
        # REMOVE WEAK SCORES
        # =========================

        if result["score"] < 0.45:
            continue

        filtered_results.append(result)

    # =========================
    # REMOVE DUPLICATES
    # =========================

    unique_results = []

    seen_names = set()

    for result in filtered_results:

        clean_name = (
            result["name"]
            .strip()
            .lower()
        )

        if clean_name not in seen_names:

            unique_results.append(result)

            seen_names.add(clean_name)

    return unique_results[:top_k]