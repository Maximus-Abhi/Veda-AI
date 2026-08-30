"use client";

import { useState } from "react";

type Region = {
  page: number;
  x: number;
  y: number;
  width: number;
  height: number;
};

type Answer = {
  question_number: string;
  text: string;
  regions: Region[];
};

type Question = {
  number: string;
  text: string;
  marks: number;
  answer: Answer | null;
  status: "answered" | "unanswered";
};

type AnswerPage = {
  page: number;
  image: string;
  width: number;
  height: number;
};

export default function Home() {
  const [questionPaper, setQuestionPaper] = useState<File | null>(null);
  const [answerSheet, setAnswerSheet] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answerPages, setAnswerPages] = useState<AnswerPage[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState(0);
  const [error, setError] = useState("");

  const handleFile = (
    event: React.ChangeEvent<HTMLInputElement>,
    type: "question" | "answer"
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please upload PDF files only.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Each file must be smaller than 10MB.");
      return;
    }

    setError("");

    if (type === "question") {
      setQuestionPaper(file);
    } else {
      setAnswerSheet(file);
    }
  };

  const startMapping = async () => {
    if (!questionPaper || !answerSheet) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();

      formData.append("question_paper", questionPaper);
      formData.append("answer_sheet", answerSheet);

   const API_URL = process.env.NEXT_PUBLIC_API_URL;

const response = await fetch(
  `${API_URL}/api/test-mapping`,
  {
    method: "POST",
    body: formData,
  }
);
      if (!response.ok) {
        throw new Error("Assessment processing failed.");
      }

      const data = await response.json();

      if (!data.questions || data.questions.length === 0) {
        throw new Error("No questions were detected.");
      }

      setQuestions(data.questions);
      setAnswerPages(data.answer_pages || []);
      setSelectedQuestion(0);
    } catch (error) {
      console.error(error);
      setError(
        "Unable to process the assessment. Please check the files and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetAssessment = () => {
    setQuestionPaper(null);
    setAnswerSheet(null);
    setQuestions([]);
    setAnswerPages([]);
    setSelectedQuestion(0);
    setError("");
  };

  if (loading) {
    return (
      <main className="loading_page">
        <div className="loading_content">
          <div className="sparkles">
            <span>✦</span>
            <span>✦</span>
            <span>✦</span>
          </div>

          <h2 className="loading_title">Extracting...</h2>

          <p className="loading_text">
            Reading the answer sheet and mapping answers...
          </p>
        </div>
      </main>
    );
  }

  if (questions.length > 0) {
    return (
      <ReviewScreen
        questions={questions}
        answerPages={answerPages}
        selectedQuestion={selectedQuestion}
        setSelectedQuestion={setSelectedQuestion}
        resetAssessment={resetAssessment}
      />
    );
  }

  return (
    <main className="app_page">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand_icon">V</div>
          <span>VedaAI</span>
        </div>

        <button className="toolkit_button">
          ✦ AI Teacher&apos;s Toolkit
        </button>

        <nav className="sidebar_nav">
          <button>
            ⌂ <span>Home</span>
          </button>
          <button>
            ⊞ <span>My Classroom</span>
          </button>
          <button>
            ▤ <span>Assignments</span>
          </button>
          <button className="active">
            ▣ <span>Exams</span>
          </button>
          <button>
            ◷ <span>My Library</span>
          </button>
        </nav>

        <div className="school_card">
          <div className="school_avatar">◉</div>

          <div>
            <strong>Delhi Public School</strong>
            <span>school workspace</span>
          </div>
        </div>
      </aside>

      <section className="upload_area">
        <header className="topbar">
          <button className="back_button">← &nbsp; Exams</button>

          <div className="teacher">
            <span>?</span>
            <span>♧</span>
            <div className="teacher_avatar">M</div>
            <span>Teacher⌄</span>
          </div>
        </header>

        <div className="upload_content">
          <h1>
            Upload{" "}
            <span>Question Paper &amp; Answer Sheets</span>
          </h1>

          <p className="upload_subtitle">
            Upload both files to get started
          </p>

          <div className="teacher_illustration">👩‍🏫</div>

          <div className="upload_cards">
            <UploadCard
              title="Question Paper"
              file={questionPaper}
              onChange={(event) => handleFile(event, "question")}
              onRemove={() => setQuestionPaper(null)}
            />

            <UploadCard
              title="Answer Sheet"
              file={answerSheet}
              onChange={(event) => handleFile(event, "answer")}
              onRemove={() => setAnswerSheet(null)}
            />
          </div>

          {error && <p className="error">{error}</p>}

          <button
            className={`start_button ${
              questionPaper && answerSheet ? "ready" : ""
            }`}
            disabled={!questionPaper || !answerSheet}
            onClick={startMapping}
          >
            ✦ &nbsp; Start Mapping &nbsp; →
          </button>

          <p className="upload_hint">
            Once both files are uploaded, you&apos;ll be able to map
            answers with questions
          </p>
        </div>
      </section>
    </main>
  );
}

function UploadCard({
  title,
  file,
  onChange,
  onRemove,
}: {
  title: string;
  file: File | null;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onRemove: () => void;
}) {
  return (
    <div className={`upload_box ${file ? "has_file" : ""}`}>
      {!file ? (
        <label className="upload_label">
          <input
            type="file"
            accept="application/pdf"
            onChange={onChange}
            hidden
          />

          <div className="upload_icon">↑</div>

          <strong>
            Upload <span>{title}</span>
          </strong>

          <small>Max 10MB</small>
        </label>
      ) : (
        <div className="file_selected">
          <div className="pdf_icon">PDF</div>

          <div className="file_details">
            <strong>{file.name}</strong>

            <span>
              PDF · {(file.size / (1024 * 1024)).toFixed(1)} MB
            </span>
          </div>

          <button
            type="button"
            onClick={onRemove}
            className="remove_file"
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
}

function ReviewScreen({
  questions,
  answerPages,
  selectedQuestion,
  setSelectedQuestion,
  resetAssessment,
}: {
  questions: Question[];
  answerPages: AnswerPage[];
  selectedQuestion: number;
  setSelectedQuestion: (index: number) => void;
  resetAssessment: () => void;
}) {
  const question = questions[selectedQuestion];

  const answered = questions.filter(
    (item) => item.status === "answered"
  ).length;

  return (
    <main className="review_page">
      <header className="review_topbar">
        <div className="brand">
          <div className="brand_icon">V</div>
          <span>VedaAI</span>
        </div>

        <div className="review_title">
          Assessment Review
        </div>
      </header>

      <div className="review_layout">
        <aside className="question_sidebar">
          <div className="question_sidebar_header">
            <h2>Questions</h2>
            <span>{questions.length} questions</span>
          </div>

          <div className="progress_text">
            {answered}/{questions.length} answered
          </div>

          <div className="question_list">
            {questions.map((item, index) => (
              <button
                key={item.number}
                className={`question_item ${
                  index === selectedQuestion ? "selected" : ""
                }`}
                onClick={() => setSelectedQuestion(index)}
              >
                <div className="question_item_top">
                  <strong>Q{item.number}</strong>

                  {item.status === "answered" ? (
                    <span className="answered_status">
                      ✓ Answered
                    </span>
                  ) : (
                    <span className="unanswered_status">
                      Unanswered
                    </span>
                  )}
                </div>

                <p>{item.text}</p>

                <small>{item.marks} marks</small>
              </button>
            ))}
          </div>
        </aside>

        <section className="review_main">
          <div className="review_header">
            <div>
              <p>Question</p>
              <h1>Q{question.number}</h1>
            </div>

            <div
              className={`review_badge ${question.status}`}
            >
              {question.status === "answered"
                ? "Answered"
                : "Unanswered"}
            </div>
          </div>

          <div className="review_card">
            <label>Question</label>

            <p>{question.text}</p>

            <div className="marks">
              {question.marks} marks
            </div>
          </div>

          <div className="review_card answer_card">
            <label>Student Answer</label>

            {question.answer ? (
              <p>{question.answer.text}</p>
            ) : (
              <p className="empty_answer">
                No answer detected for this question.
              </p>
            )}
          </div>

          {question.answer && answerPages.length > 0 && (
            <AnswerSheet
              answer={question.answer}
              pages={answerPages}
            />
          )}
        </section>
      </div>

      <button
        className="floating_back"
        onClick={resetAssessment}
      >
        ←
      </button>
    </main>
  );
}

function AnswerSheet({
  answer,
  pages,
}: {
  answer: Answer;
  pages: AnswerPage[];
}) {
  const region = answer.regions?.[0];

  const page = pages.find(
    (item) => item.page === region?.page
  );

  if (!page) return null;

  return (
    <div className="review_card answer_sheet_card">
      <div className="answer_sheet_header">
        <label>Answer Sheet</label>

        <span>
          Page {page.page} of {pages.length}
        </span>
      </div>

      <div className="sheet_viewer">
        <div className="sheet_image_wrapper">
          <img
            src={`data:image/png;base64,${page.image}`}
            className="sheet_image"
            alt={`Answer sheet page ${page.page}`}
          />

          {region && (
            <div
              className="answer_highlight"
              style={{
                left: `${region.x * 100}%`,
                top: `${region.y * 100}%`,
                width: `${region.width * 100}%`,
                height: `${region.height * 100}%`,
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
}