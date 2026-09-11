from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/")
def list_transactions():
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
        "transactions.html",
        transactions=transactions,
        accounts=account_service.get_all_accounts(),
        categories=category_service.get_all_categories(),
        filters={"month": month, "account_id": account_id,
                 "category_id": category_id, "type": type_}
    )


@transactions_bp.route("/add", methods=["GET", "POST"])
def add_transaction():
    account_service = current_app.config["ACCOUNT_SERVICE"]
    category_service = current_app.config["CATEGORY_SERVICE"]
    tx_service = current_app.config["TRANSACTION_SERVICE"]

    if request.method == "POST":
        try:
            category_id = request.form.get("category_id")
            category_id = int(category_id) if category_id else None
            tx_service.create_transaction(
                account_id=int(request.form["account_id"]),
                category_id=category_id,
                type_=request.form["type"],
                amount=float(request.form["amount"]),
                description=request.form.get("description", ""),
                date=request.form["date"]
            )
            flash("Transaction added!", "success")
            return redirect(url_for("transactions.list_transactions"))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")

    return render_template(
        "transaction_form.html",
        transaction=None,
        accounts=account_service.get_all_accounts(),
        categories=category_service.get_all_categories()
    )


@transactions_bp.route("/edit/<int:tx_id>", methods=["GET", "POST"])
def edit_transaction(tx_id):
    account_service = current_app.config["ACCOUNT_SERVICE"]
    category_service = current_app.config["CATEGORY_SERVICE"]
    tx_service = current_app.config["TRANSACTION_SERVICE"]

    tx = tx_service.get_transaction(tx_id)
    if not tx:
        flash("Transaction not found.", "error")
        return redirect(url_for("transactions.list_transactions"))

    if request.method == "POST":
        try:
            category_id = request.form.get("category_id")
            category_id = int(category_id) if category_id else None
            tx_service.update_transaction(
                tx_id=tx_id,
                account_id=int(request.form["account_id"]),
                category_id=category_id,
                type_=request.form["type"],
                amount=float(request.form["amount"]),
                description=request.form.get("description", ""),
                date=request.form["date"]
            )
            flash("Transaction updated!", "success")
            return redirect(url_for("transactions.list_transactions"))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")

    return render_template(
        "transaction_form.html",
        transaction=tx,
        accounts=account_service.get_all_accounts(),
        categories=category_service.get_all_categories()
    )


@transactions_bp.route("/delete/<int:tx_id>", methods=["POST"])
def delete_transaction(tx_id):
    if current_app.config["TRANSACTION_SERVICE"].delete_transaction(tx_id):
        flash("Transaction deleted.", "success")
    else:
        flash("Transaction not found.", "error")
    return redirect(url_for("transactions.list_transactions"))