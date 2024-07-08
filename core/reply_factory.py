
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    ry:
        if current_question_id is not None:
            answers = session.get("answers", {})
            answers[current_question_id] = answer
            session["answers"] = answers
            return True, ""
        return False, "Invalid question ID."
    except Exception as e:
        return False, str(e)
    


def get_next_question(current_question_id):
    try:
        current_index = None
        for index, question in enumerate(PYTHON_QUESTION_LIST):
            if question["id"] == current_question_id:
                current_index = index
                break

        if current_index is not None and current_index + 1 < len(PYTHON_QUESTION_LIST):
            next_question = PYTHON_QUESTION_LIST[current_index + 1]
            return next_question["question"], next_question["id"]
        return None, None
    except Exception as e:
        return None, None


def generate_final_response(session):
    answers = session.get("answers", {})
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question in PYTHON_QUESTION_LIST:
        qid = question["id"]
        correct_answer = question.get("correct_answer")
        user_answer = answers.get(qid)

        if user_answer and user_answer.lower() == correct_answer.lower():
            score += 1

    result_message = f"You've completed the quiz! Your score is {score}/{total_questions}."
    return result_message
