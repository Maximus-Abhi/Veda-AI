import os
import json
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1")


def extract_answers(page_images):
    images = []

    for page_data in page_images:
        image_bytes = page_data["image"]
        image_data = (
            "data:image/png;base64,"
            + base64.b64encode(image_bytes).decode("utf-8"))

        images.append({"page": page_data["page"],"url": image_data})

    prompt = """
Extract every student answer visible in these answer-sheet pages.

Rules:

1. Preserve the question number written by the student.
2. Return answers in the order they appear.
3. The question number may be written as Q1, Q2, 1, 2, etc.
4. Normalize question numbers to Q1, Q2, Q3, etc.
5. Do not invent answers.
6. Include only answers actually visible.
7. Extract the student's answer text as accurately as possible.
8. For each answer, provide the page number.
9. Return approximate normalized coordinates of the answer region.
10. Coordinates must be between 0 and 1.
11. Return only valid JSON.
12. Do not use markdown.
13. Do not wrap the JSON in ```json or ```.

Return exactly:

{
    "answers": [
        {
            "question_number": "Q1",
            "text": "student answer",
            "regions": [
                {
                    "page": 1,
                    "x": 0.1,
                    "y": 0.2,
                    "width": 0.4,
                    "height": 0.05
                }
            ]
        }
    ]
}
"""

    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    for image in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": image["url"]}})

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": content
            }])
    response_text = response.choices[0].message.content

    if not response_text:
        print("Empty response from model")
        return []

    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        print("Invalid JSON response:")
        print(response_text)
        return []

    answers = data.get("answers", [])

    for answer in answers:
        question_number = str(answer.get("question_number", "")).strip()
        question_number = question_number.replace("Question ","").replace("question ","")
        question_number = question_number.replace( "Q","").strip()

        if question_number.isdigit():
            answer["question_number"] = f"Q{question_number}"
    return answers