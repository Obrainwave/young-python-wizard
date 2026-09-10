from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

admin = Blueprint("admin", __name__)


@admin.route("/")
def dashboard():
    quizzes = current_app.config["QUIZ_SERVICE"].get_all_quizzes()
    # Add question count for each quiz
    quiz_data = []
    for q in quizzes:
        count = current_app.config["QUIZ_SERVICE"].count_questions(q.id)
        quiz_data.append({"quiz": q, "question_count": count})
    return render_template("admin_dashboard.html", quiz_data=quiz_data)


@admin.route("/quiz/add", methods=["GET", "POST"])
def add_quiz():
    if request.method == "POST":
        try:
            current_app.config["QUIZ_SERVICE"].create_quiz(
                title=request.form["title"],
                description=request.form.get("description", "")
            )
            flash("Quiz created successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("quiz_form.html", quiz=None)


@admin.route("/quiz/edit/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = current_app.config["QUIZ_SERVICE"].get_quiz(quiz_id)
    if not quiz:
        flash("Quiz not found.", "error")
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        try:
            current_app.config["QUIZ_SERVICE"].update_quiz(
                quiz_id=quiz_id,
                title=request.form["title"],
                description=request.form.get("description", "")
            )
            flash("Quiz updated!", "success")
            return redirect(url_for("admin.dashboard"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("quiz_form.html", quiz=quiz)


@admin.route("/quiz/delete/<int:quiz_id>", methods=["POST"])
def delete_quiz(quiz_id):
    if current_app.config["QUIZ_SERVICE"].delete_quiz(quiz_id):
        flash("Quiz deleted.", "success")
    else:
        flash("Quiz not found.", "error")
    return redirect(url_for("admin.dashboard"))


@admin.route("/quiz/<int:quiz_id>/questions")
def manage_questions(quiz_id):
    quiz = current_app.config["QUIZ_SERVICE"].get_quiz(quiz_id)
    if not quiz:
        flash("Quiz not found.", "error")
        return redirect(url_for("admin.dashboard"))
    questions = current_app.config["QUIZ_SERVICE"].get_questions_for_quiz(quiz_id)
    return render_template("question_list.html", quiz=quiz, questions=questions)


@admin.route("/quiz/<int:quiz_id>/question/add", methods=["GET", "POST"])
def add_question(quiz_id):
    quiz = current_app.config["QUIZ_SERVICE"].get_quiz(quiz_id)
    if not quiz:
        flash("Quiz not found.", "error")
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        try:
            options = [request.form[f"option_{i}"] for i in range(4)]
            correct_index = int(request.form["correct_index"])
            current_app.config["QUIZ_SERVICE"].add_question(
                quiz_id=quiz_id,
                text=request.form["text"],
                options=options,
                correct_index=correct_index
            )
            flash("Question added!", "success")
            return redirect(url_for("admin.manage_questions", quiz_id=quiz_id))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("question_form.html", quiz=quiz, question=None)


@admin.route("/question/edit/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    question = current_app.config["QUIZ_SERVICE"].get_question(question_id)
    if not question:
        flash("Question not found.", "error")
        return redirect(url_for("admin.dashboard"))
    quiz = current_app.config["QUIZ_SERVICE"].get_quiz(question.quiz_id)
    if request.method == "POST":
        try:
            options = [request.form[f"option_{i}"] for i in range(4)]
            correct_index = int(request.form["correct_index"])
            current_app.config["QUIZ_SERVICE"].update_question(
                question_id=question_id,
                text=request.form["text"],
                options=options,
                correct_index=correct_index
            )
            flash("Question updated!", "success")
            return redirect(url_for("admin.manage_questions", quiz_id=quiz.id))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("question_form.html", quiz=quiz, question=question)


@admin.route("/question/delete/<int:question_id>", methods=["POST"])
def delete_question(question_id):
    question = current_app.config["QUIZ_SERVICE"].get_question(question_id)
    if not question:
        flash("Question not found.", "error")
        return redirect(url_for("admin.dashboard"))
    quiz_id = question.quiz_id
    current_app.config["QUIZ_SERVICE"].delete_question(question_id)
    flash("Question deleted.", "success")
    return redirect(url_for("admin.manage_questions", quiz_id=quiz_id))