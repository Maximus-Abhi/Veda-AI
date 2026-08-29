from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.question_extractor import extract_questions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/api/assessment")
async def create_assessment(question_paper: UploadFile = File(...),answer_sheet: UploadFile = File(...)):

    question_bytes = await question_paper.read()
    answer_bytes = await answer_sheet.read()

    question_pages = convert_pdf_to_images(question_bytes)
    answer_pages = convert_pdf_to_images(answer_bytes)

    questions = extract_questions(question_pages)

    return {"questions": questions,"question_paper": {"name": question_paper.filename,"pages": len(question_pages),},
        "answer_sheet": {"name": answer_sheet.filename,"pages": len(answer_pages),},}