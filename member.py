from flask import Blueprint, render_template, redirect, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database import get_db

member_bp = Blueprint("member", __name__, url_prefix="/member")


def member_only():
    claims = get_jwt()
    return claims.get("role") == "member"


@member_bp.route("/dashboard")
@jwt_required()
def dashboard():
    if not member_only():
        return render_template("403.html"), 403
    return render_template("member/dashboard.html")


@member_bp.route("/books")
@jwt_required()
def books():
    if not member_only():
        return render_template("403.html"), 403

    db = get_db()
    books = db.execute("SELECT * FROM books WHERE available=1").fetchall()
    return render_template("member/books.html", books=books)


@member_bp.route("/borrow/<int:book_id>")
@jwt_required()
def borrow(book_id):
    if not member_only():
        return render_template("403.html"), 403

    user_id = get_jwt_identity()
    db = get_db()

    db.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
    db.execute(
        "INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)",
        (user_id, book_id),
    )
    db.commit()

    flash("Book borrowed successfully")
    return redirect("/member/books")
