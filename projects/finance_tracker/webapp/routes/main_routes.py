from datetime import date
from flask import Blueprint, render_template, request, current_app

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Dashboard with totals, monthly summary, budgets, and recent transactions."""
    account_service = current_app.config["ACCOUNT_SERVICE"]
    tx_service = current_app.config["TRANSACTION_SERVICE"]
    budget_service = current_app.config["BUDGET_SERVICE"]

    # Total balance across all accounts
    total_balance = account_service.get_total_balance()

    # Current month
    today = date.today()
    current_month = today.strftime("%Y-%m")
    summary = tx_service.monthly_summary(current_month)

    # Budgets for this month
    budgets = budget_service.get_budgets_with_progress(current_month)

    # Recent transactions
    recent = tx_service.get_recent(limit=5)

    # Account balances for display
    account_balances = account_service.get_all_with_balances()

    return render_template(
        "index.html",
        total_balance=total_balance,
        summary=summary,
        budgets=budgets,
        recent=recent,
        account_balances=account_balances,
        current_month=current_month
    )


@main.route("/reports")
def reports():
    """Advanced filterable transaction view."""
    tx_service = current_app.config["TRANSACTION_SERVICE"]
    account_service = current_app.config["ACCOUNT_SERVICE"]
    category_service = current_app.config["CATEGORY_SERVICE"]

    month = request.args.get("month", "")
    account_id = request.args.get("account_id", type=int)
    category_id = request.args.get("category_id", type=int)
    type_ = request.args.get("type", "")

    transactions = tx_service.get_transactions(
        month=month or None,
        account_id=account_id,
        category_id=category_id,
        type_=type_ or None
    )

    return render_template(
        "reports.html",
        transactions=transactions,
        accounts=account_service.get_all_accounts(),
        categories=category_service.get_all_categories(),
        filters={"month": month, "account_id": account_id,
                 "category_id": category_id, "type": type_}
    )