import os
import json

from google import genai
from google.genai import types

from dotenv import load_dotenv


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_questions(page_images):
    questions = []

    for page_data in page_images:
        page_number = page_data["page"]
        image_bytes = page_data["image"]

        prompt = """
Extract every question from this question paper page.

Rules:

1. Preserve the exact original question numbering.
2. Keep questions in the same printed order.
3. Treat labelled sub-parts as separate questions.

Example:
11(a) must be one question.
11(b) must be another question.

4. Do not change question numbers.
5. Do not create questions that are not visible.
6. If marks are visible, extract them.
7. Return only valid JSON.

Return this format:

{
    "questions": [
        {
            "number": "1",
            "text": "question text",
            "marks": 2
        },
        {
            "number": "11(a)",
            "text": "question text",
            "marks": 3
        }
    ]
}

If marks are not visible, use null.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/png"
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        data = json.loads(response.text)

        for question in data.get("questions", []):
            question["page"] = page_number
            question["order"] = len(questions) + 1

            questions.append(question)

    return questions