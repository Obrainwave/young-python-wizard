from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

main = Blueprint("main", __name__)


@main.route("/")
def index():
    quizzes = current_app.config["QUIZ_SERVICE"].get_all_quizzes()
    return render_template("index.html", quizzes=quizzes)


@main.route("/quizzes")
def quiz_list():
    quizzes = current_app.config["QUIZ_SERVICE"].get_all_quizzes()
    return render_template("quiz_list.html", quizzes=quizzes)


@main.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
def take_quiz(quiz_id):
    quiz_service = current_app.config["QUIZ_SERVICE"]
    attempt_service = current_app.config["ATTEMPT_SERVICE"]

    quiz = quiz_service.get_quiz(quiz_id)
    if not quiz:
        flash("Quiz not found.", "error")
        return redirect(url_for("main.quiz_list"))

    questions = quiz_service.get_questions_for_quiz(quiz_id)
    if not questions:
        flash("This quiz has no questions yet.", "warning")
        return redirect(url_for("main.quiz_list"))

    if request.method == "POST":
        user_name = request.form.get("user_name", "").strip()
        if not user_name:
            flash("Please enter your name.", "error")
            return render_template("take_quiz.html", quiz=quiz, questions=questions)

        answers = {}
        for q in questions:
            raw = request.form.get(f"q_{q.id}")
            if raw:
                try:
                    answers[q.id] = int(raw)
                except ValueError:
                    pass

        try:
            attempt = attempt_service.submit_attempt(quiz_id, user_name, answers)
        except ValueError as e:
            flash(str(e), "error")
            return render_template("take_quiz.html", quiz=quiz, questions=questions)

        return redirect(url_for("main.quiz_result", attempt_id=attempt.id))

    # GET: Show name entry and quiz questions in one page
    return render_template("take_quiz.html", quiz=quiz, questions=questions)


@main.route("/result/<int:attempt_id>")
def quiz_result(attempt_id):
    attempt_service = current_app.config["ATTEMPT_SERVICE"]
    quiz_service = current_app.config["QUIZ_SERVICE"]

    attempt, details = attempt_service.get_detailed_results(attempt_id, quiz_service)
    if not attempt:
        flash("Result not found.", "error")
        return redirect(url_for("main.quiz_list"))

    quiz = quiz_service.get_quiz(attempt.quiz_id)
    return render_template("quiz_result.html", attempt=attempt, quiz=quiz, details=details)


@main.route("/quiz/<int:quiz_id>/leaderboard")
def leaderboard(quiz_id):
    quiz_service = current_app.config["QUIZ_SERVICE"]
    attempt_service = current_app.config["ATTEMPT_SERVICE"]

    quiz = quiz_service.get_quiz(quiz_id)
    if not quiz:
        flash("Quiz not found.", "error")
        return redirect(url_for("main.quiz_list"))

    top_attempts = attempt_service.get_leaderboard(quiz_id, limit=10)
    return render_template("leaderboard.html", quiz=quiz, attempts=top_attempts)