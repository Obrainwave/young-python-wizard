from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/")
def list_accounts():
    data = current_app.config["ACCOUNT_SERVICE"].get_all_with_balances()
    return render_template("accounts.html", data=data)


@accounts_bp.route("/add", methods=["GET", "POST"])
def add_account():
    if request.method == "POST":
        try:
            current_app.config["ACCOUNT_SERVICE"].create_account(
                name=request.form["name"],
                account_type=request.form["account_type"],
                initial_balance=float(request.form.get("initial_balance", 0)),
                currency=request.form.get("currency", "USD")
            )
            flash("Account created successfully!", "success")
            return redirect(url_for("accounts.list_accounts"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("account_form.html", account=None)


@accounts_bp.route("/edit/<int:account_id>", methods=["GET", "POST"])
def edit_account(account_id):
    account = current_app.config["ACCOUNT_SERVICE"].get_account(account_id)
    if not account:
        flash("Account not found.", "error")
        return redirect(url_for("accounts.list_accounts"))
    if request.method == "POST":
        try:
            current_app.config["ACCOUNT_SERVICE"].update_account(
                account_id=account_id,
                name=request.form["name"],
                account_type=request.form["account_type"],
                initial_balance=float(request.form.get("initial_balance", 0)),
                currency=request.form.get("currency", "USD")
            )
            flash("Account updated!", "success")
            return redirect(url_for("accounts.list_accounts"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("account_form.html", account=account)


@accounts_bp.route("/<int:account_id>")
def account_detail(account_id):
    account_service = current_app.config["ACCOUNT_SERVICE"]
    tx_service = current_app.config["TRANSACTION_SERVICE"]
    account = account_service.get_account(account_id)
    if not account:
        flash("Account not found.", "error")
        return redirect(url_for("accounts.list_accounts"))
    balance = account_service.get_account_balance(account_id)
    transactions = tx_service.get_transactions(account_id=account_id)
    return render_template("account_detail.html",
                           account=account, balance=balance, transactions=transactions)


@accounts_bp.route("/delete/<int:account_id>", methods=["POST"])
def delete_account(account_id):
    if current_app.config["ACCOUNT_SERVICE"].delete_account(account_id):
        flash("Account and its transactions deleted.", "success")
    else:
        flash("Account not found.", "error")
    return redirect(url_for("accounts.list_accounts"))