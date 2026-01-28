from flask import Blueprint, render_template, redirect, flash, request
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_only():
    return get_jwt().get("role") == "admin"


@admin_bp.route("/dashboard")
@jwt_required()
def dashboard():
    if not admin_only():
        return render_template("403.html"), 403
    return render_template("admin/dashboard.html")


@admin_bp.route("/books", methods=["GET", "POST"])
@jwt_required()
def books():
    if not admin_only():
        return render_template("403.html"), 403

    db = get_db()

    if request.method == "POST":
        db.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
            (request.form["title"], request.form["author"]),
        )
        db.commit()
        flash("Book added successfully")
        return redirect("/admin/books")

    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("admin/books.html", books=books)
