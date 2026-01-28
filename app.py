from flask import Flask
from flask_jwt_extended import JWTManager
from database import init_db
from auth import auth_bp
from admin import admin_bp
from member import member_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config["JWT_SECRET_KEY"] = "jwt-secret"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(member_bp)


@app.route("/")
def home():
    return "<h3>Go to <a href='/login'>Login</a></h3>"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
