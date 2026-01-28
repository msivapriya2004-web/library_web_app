from flask import Blueprint, render_template, request, redirect, flash
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
)
import bcrypt
from database import get_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()

        if user and bcrypt.checkpw(password, user["password"]):
            token = create_access_token(
                identity=str(user["id"]),
                additional_claims={"role": user["role"], "username": user["username"]},
            )
            resp = redirect(
                "/admin/dashboard" if user["role"] == "admin" else "/member/dashboard"
            )
            set_access_cookies(resp, token)
            return resp

        flash("Invalid username or password")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())
        role = request.form["role"]

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )
            db.commit()
            flash("Registration successful")
            return redirect("/login")
        except:
            flash("Username already exists")

    return render_template("register.html")


@auth_bp.route("/logout")
@jwt_required()
def logout():
    resp = redirect("/login")
    unset_jwt_cookies(resp)
    return resp
