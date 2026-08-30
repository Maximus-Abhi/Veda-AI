def clean_question_number(question_number):

    if not question_number:
        return None

    question_number = question_number.strip()
    question_number = question_number.replace("Q", "")
    question_number = question_number.replace("q", "")
    question_number = question_number.replace(" ", "")
    question_number = question_number.replace(".", "")
    return question_number


def map_questions(questions, answers):
    answer_map = {}

    for answer in answers:
        question_number = clean_question_number(answer["question_number"])

        if question_number:
            answer_map[question_number] = answer
    mapped_questions = []

    for question in questions:
        question_number = question["number"]
        clean_number = clean_question_number(question_number)

        if clean_number in answer_map:
            mapped_questions.append({

                "number": question_number,
                "text": question["text"],
                "marks": question["marks"],
                "answer": answer_map[clean_number],
                "status": "answered"})

        else:
            mapped_questions.append({

                "number": question_number,
                "text": question["text"],
                "marks": question["marks"],
                "answer": None,
                "status": "unanswered"})

    return mapped_questions