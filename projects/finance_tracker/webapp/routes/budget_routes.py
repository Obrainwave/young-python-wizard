from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.route("/")
def list_budgets():
    month = request.args.get("month") or date.today().strftime("%Y-%m")
    budgets = current_app.config["BUDGET_SERVICE"].get_budgets_with_progress(month)
    return render_template("budgets.html", budgets=budgets, month=month)


@budgets_bp.route("/add", methods=["GET", "POST"])
def add_budget():
    category_service = current_app.config["CATEGORY_SERVICE"]
    budget_service = current_app.config["BUDGET_SERVICE"]

    if request.method == "POST":
        try:
            budget_service.set_budget(
                category_id=int(request.form["category_id"]),
                month=request.form["month"],
                amount=float(request.form["amount"])
            )
            flash("Budget saved!", "success")
            return redirect(url_for("budgets.list_budgets", month=request.form["month"]))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")

    return render_template(
        "budget_form.html",
        budget=None,
        expense_categories=category_service.get_expense_categories(),
        default_month=date.today().strftime("%Y-%m")
    )


@budgets_bp.route("/edit/<int:budget_id>", methods=["GET", "POST"])
def edit_budget(budget_id):
    category_service = current_app.config["CATEGORY_SERVICE"]
    budget_service = current_app.config["BUDGET_SERVICE"]

    budget = budget_service.get_budget(budget_id)
    if not budget:
        flash("Budget not found.", "error")
        return redirect(url_for("budgets.list_budgets"))

    if request.method == "POST":
        try:
            budget_service.set_budget(
                category_id=int(request.form["category_id"]),
                month=request.form["month"],
                amount=float(request.form["amount"])
            )
            flash("Budget updated!", "success")
            return redirect(url_for("budgets.list_budgets", month=request.form["month"]))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")

    return render_template(
        "budget_form.html",
        budget=budget,
        expense_categories=category_service.get_expense_categories(),
        default_month=budget.month
    )


@budgets_bp.route("/delete/<int:budget_id>", methods=["POST"])
def delete_budget(budget_id):
    month = request.form.get("month")
    if current_app.config["BUDGET_SERVICE"].delete_budget(budget_id):
        flash("Budget removed.", "success")
    else:
        flash("Budget not found.", "error")
    return redirect(url_for("budgets.list_budgets", month=month))