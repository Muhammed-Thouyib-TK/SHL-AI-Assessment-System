import os
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# CONFIGURE GEMINI
# =========================

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# LOAD MODEL
# =========================

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =========================
# GENERATE REPLY
# =========================

def generate_reply(user_message, recommendations=None):

    rec_text = ""

    # Add SHL recommendations
    if recommendations:

        rec_text = "\nRecommended SHL Assessments:\n"

        for rec in recommendations[:5]:

            rec_text += (
                f"- {rec['name']} "
                f"({rec['test_type']})\n"
            )

    # Prompt
    prompt = f"""
You are an SHL assessment recommendation assistant.

Your responsibilities:
- Explain why the recommended SHL assessments fit the hiring requirement.
- Only use assessments provided in the recommendation list.
- Never invent assessments.
- Keep response concise and professional.
- Keep response under 100 words.

User Query:
{user_message}

{rec_text}

Generate a professional recommendation summary.
"""

    try:

        response = model.generate_content(prompt)

        # Safe extraction
        if hasattr(response, "text") and response.text:

            return response.text.strip()

        # Fallback if Gemini gives empty output
        return (
            "I found suitable SHL assessments "
            "based on the provided role, skills, "
            "and hiring requirements."
        )

    except Exception as e:

        print("Gemini Error:", e)

        return (
            "I found suitable SHL assessments "
            "based on the provided role and skills."
        )