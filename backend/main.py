import base64

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.answer_extractor import extract_answers
from services.question_extractor import extract_questions
from services.mapper import map_questions
from services.pdf_service import convert_pdf_to_images
from services.pdf_service import convert_pdf_to_base64_images
from services.pdf_service import extract_pdf_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/api/assessment")
async def create_assessment(
    question_paper: UploadFile = File(...),
    answer_sheet: UploadFile = File(...),):
    question_bytes = await question_paper.read()
    answer_bytes = await answer_sheet.read()

    question_pages = extract_pdf_text(question_bytes)
    answer_pages = convert_pdf_to_images(answer_bytes)
    questions = extract_questions(question_pages)

    return {"questions": questions,"question_paper": {"name": question_paper.filename,"pages": len(question_pages),},
        "answer_sheet": {"name": answer_sheet.filename,"pages": len(answer_pages),},}


@app.post("/api/test-answers")
async def test_answers(
    answer_sheet: UploadFile = File(...),):
    answer_bytes = await answer_sheet.read()
    answer_pages = convert_pdf_to_images(answer_bytes)
    answers = extract_answers(answer_pages)

    return {"file_name": answer_sheet.filename,"pages": len(answer_pages),"answers": answers,}





@app.post("/api/test-mapping")
async def test_mapping(
    question_paper: UploadFile = File(...),
    answer_sheet: UploadFile = File(...)
):
    question_bytes = await question_paper.read()
    answer_bytes = await answer_sheet.read()

    question_pages = extract_pdf_text(question_bytes)
    answer_pages = convert_pdf_to_images(answer_bytes)

    questions = extract_questions(question_pages)
    answers = extract_answers(answer_pages)

    mapped_questions = map_questions(questions, answers)

    encoded_pages = []

    for page in answer_pages:
        encoded_pages.append({
            "page": page["page"],
            "image": base64.b64encode(page["image"]).decode("utf-8"),
            "width": page.get("width", 0),
            "height": page.get("height", 0),
        })

    return {
        "questions": mapped_questions,
        "answer_pages": encoded_pages,
    }