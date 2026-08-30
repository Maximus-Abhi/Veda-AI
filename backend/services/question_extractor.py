import re


def extract_questions(page_texts):
    questions = []
    full_text = ""

    for page_data in page_texts:
        page_number = page_data["page"]
        text = page_data.get("text", "")
        full_text += f"\n[[PAGE:{page_number}]]\n"
        full_text += text

    section_a_matches = list(re.finditer(r"\bSection\s+A\b",full_text,flags=re.IGNORECASE))

    if len(section_a_matches) >= 2:
        question_text = full_text[section_a_matches[1].end():]
    else:
        question_text = full_text

    pattern = re.compile(r"(?m)^\s*(\d{1,2})\.\s*")
    matches = list(pattern.finditer(question_text))

    for index, match in enumerate(matches):
        number = match.group(1)
        number_int = int(number)

        if number_int < 1 or number_int > 38:
            continue

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(question_text)

        raw_question = question_text[start:end]
        before_question = question_text[:match.start()]
        page_matches = re.findall(r"\[\[PAGE:(\d+)\]\]",before_question)

        page_number = (
            int(page_matches[-1])
            if page_matches
            else 1
        )

        text = clean_question_text(raw_question)

        if not text:
            continue

        if any(q["number"] == number for q in questions):
            continue

        questions.append({
            "number": number,
            "text": text,
            "marks": get_default_marks(number_int),
            "page": page_number,
            "order": len(questions) + 1,
        })

    return questions


def clean_question_text(text):
    text = re.sub(r"\[\[PAGE:\d+\]\]", "", text)
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            lines.append(line)

    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+(?:1\s+1\s+2|1\s+1\s+2\s+2)$", "", text)
    return text.strip()

def get_default_marks(number):
    if 1 <= number <= 20:
        return 1

    if 21 <= number <= 25:
        return 2

    if 26 <= number <= 31:
        return 3

    if 32 <= number <= 35:
        return 5

    if 36 <= number <= 38:
        return 4

    return None