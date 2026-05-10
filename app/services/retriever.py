import json
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")


with open("app/data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)


assessment_texts = []

for assessment in assessments:

    text = f"""
    {assessment.get('name', '')}
    {assessment.get('test_type', '')}
    {assessment.get('description', '')}
    """

    assessment_texts.append(text)


assessment_embeddings = model.encode(
    assessment_texts,
    convert_to_tensor=True
)


def retrieve_assessments(query, top_k=5):

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        query_embedding,
        assessment_embeddings
    )[0]

    top_results = similarities.topk(k=top_k)

    recommendations = []

    for score, idx in zip(
        top_results.values,
        top_results.indices
    ):

        assessment = assessments[idx]

        recommendations.append({
            "name": assessment.get("name", "Unknown"),
            "url": assessment.get("link", ""),
            "test_type": ", ".join(assessment.get("keys", [])),
            "score": round(float(score), 2)
        })

    recommendations = sorted(
    recommendations,
    key=lambda x: x["score"],
    reverse=True
)

    blocked_keywords = [
        "front end",
        "sales",
        "marketing",
        "finance",
        "manager report",
        "participant report"
    ]

    recommendations = [
        r for r in recommendations
        if not any(
            keyword in r["name"].lower()
            for keyword in blocked_keywords
        )
    ]

    recommendations = [
        r for r in recommendations
        if r["score"] > 0.30
    ]

    return recommendations