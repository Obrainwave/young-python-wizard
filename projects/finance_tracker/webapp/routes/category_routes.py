from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/")
def list_categories():
    cats = current_app.config["CATEGORY_SERVICE"].get_all_categories()
    return render_template("categories.html", categories=cats)


@categories_bp.route("/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        try:
            current_app.config["CATEGORY_SERVICE"].create_category(
                name=request.form["name"],
                type_=request.form["type"],
                color=request.form.get("color", "#6c757d")
            )
            flash("Category added!", "success")
            return redirect(url_for("categories.list_categories"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("category_form.html", category=None)


@categories_bp.route("/edit/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    cat = current_app.config["CATEGORY_SERVICE"].get_category(category_id)
    if not cat:
        flash("Category not found.", "error")
        return redirect(url_for("categories.list_categories"))
    if request.method == "POST":
        try:
            current_app.config["CATEGORY_SERVICE"].update_category(
                category_id=category_id,
                name=request.form["name"],
                type_=request.form["type"],
                color=request.form.get("color", "#6c757d")
            )
            flash("Category updated!", "success")
            return redirect(url_for("categories.list_categories"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("category_form.html", category=cat)


@categories_bp.route("/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    if current_app.config["CATEGORY_SERVICE"].delete_category(category_id):
        flash("Category deleted.", "success")
    else:
        flash("Category not found.", "error")
    return redirect(url_for("categories.list_categories"))