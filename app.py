from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
)
from flask.sansio.app import App
from flask.testing import FlaskClient
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Admin, Ranking, Applicant
from decimal import Decimal
import os
import time
import click
import json

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

app.config.from_object(Config)

if os.getenv("VERCEL"):
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

HISTORY_LIMIT = 48


def init_db():
    with app.app_context():
        db.create_all()


def ensure_tables():
    """Create tables if missing. Returns an error string or None."""
    try:
        db.create_all()
        return None
    except Exception as exc:
        app.logger.exception("ensure_tables failed")
        return str(exc)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

app.json_encoder = DecimalEncoder

def maybe_bootstrap_admin():
    """Optional: set BOOTSTRAP_ADMIN_USER + BOOTSTRAP_ADMIN_PASSWORD in Vercel once."""
    user = os.getenv("BOOTSTRAP_ADMIN_USER")
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")
    if not user or not password:
        return
    try:
        if Admin.query.count() > 0:
            return
        admin = Admin(username=user.strip()[:64])
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Bootstrapped admin user: %s", user)
    except Exception:
        app.logger.exception("bootstrap admin failed")
        db.session.rollback()

def determine_rank(score: int) -> str:
    if  score < 50:
        return "No Rank"
    elif 50 <= score < 55:
        return "Base"
    elif 55 <= score < 60:
        return "Bronze"
    elif 60 <= score < 65:
        return "Silver"
    elif 65 <= score < 70:
        return "Gold"
    elif 70 <= score < 75:
        return "Amethyst"
    elif 75 <= score < 80:
        return "Platinum"
    elif 80 <= score < 85:
        return "Sapphire"
    elif 85 <= score < 90:
        return "Diamond"
    elif 90 <= score < 95:
        return "Emerald"
    else:
        return "Ruby"

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Admin, int(user_id))
    except (TypeError, ValueError):
        return None


@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith("/api/"):
        return jsonify({"error": "Login required"}), 401
    return redirect(url_for("login"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/benefits")
def benefits():
    return render_template("benefits.html")

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

def _config_error():
    if not app.config.get("SECRET_KEY"):
        return "SECRET_KEY is not set on the server"
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        return "DATABASE_URL is not set on the server"
    return None


@app.route("/api/health")
def api_health():
    err = _config_error()
    if err:
        return jsonify({"ok": False, "error": err}), 503
    try:
        db.session.execute(db.text("SELECT 1"))
        table_err = ensure_tables()
        maybe_bootstrap_admin()
        admin_count = Admin.query.count()
        payload = {
            "ok": table_err is None,
            "db": True,
            "tables_ok": table_err is None,
            "admin_count": admin_count,
        }
        if table_err:
            payload["error"] = table_err
        elif admin_count == 0:
            payload["hint"] = (
                "No admin users. Run: flask --app app create-admin USER PASS "
                "with production DATABASE_URL, or set BOOTSTRAP_ADMIN_USER and "
                "BOOTSTRAP_ADMIN_PASSWORD in Vercel temporarily."
            )
        status = 503 if table_err else 200
        return jsonify(payload), status
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 503


@app.route("/api/login", methods=["POST"])
def api_login():
    err = _config_error()
    if err:
        return jsonify({"error": err}), 503

    table_err = ensure_tables()
    if table_err:
        return jsonify({"error": "Tables not ready: " + table_err}), 503

    maybe_bootstrap_admin()

    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        admin = Admin.query.filter_by(username=username).first()
    except Exception as exc:
        app.logger.exception("login database error")
        return jsonify({"error": "Database error: " + str(exc)}), 503

    if not admin:
        if not os.getenv("VERCEL"):
            time.sleep(1)
        return jsonify({
            "error": "Invalid username (no admin in this database — check /api/health admin_count)",
        }), 401

    if not admin.check_password(password):
        if not os.getenv("VERCEL"):
            time.sleep(1)
        return jsonify({"error": "Invalid password"}), 401

    session.permanent = True
    login_user(admin)
    return jsonify({"success": True, "username": admin.username})

@app.route("/api/rankings")
def api_rankings():
    for applicant in Applicant.query.all():
        if applicant.done:
            if Ranking.query.filter_by(username=applicant.username).first():
                continue
            ranking = Ranking(username=applicant.username,bank_account_number=applicant.bank_account_number, ranking=determine_rank(applicant.score))
            db.session.add(ranking)
            db.session.commit()
    return jsonify([ranking.to_dict() for ranking in Ranking.query.order_by(Ranking.ranking.asc()).all() if ranking.username != "admin"])

@app.route("/api/ranking", methods=["POST"])
def api_ranking():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"error": "Username is required"}, 400)
    if not Applicant.query.filter_by(username=username).first():
        return jsonify({"error": "Username not found"}, 404)
    return jsonify({
        "ranking": determine_rank(Applicant.query.filter_by(username=username).first().score)
    })

@app.route("/api/ranking/session", methods=["POST"])
def ranking_session():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()[:64]
    bank_raw = data.get("bank_account_number")

    if not username:
        return jsonify({"error": "Username required"}, 400)

    try:
        bank_account_number = int(bank_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Valid bank account number required"}, 400)

    user = User.query.filter_by(
        username=username,
        bank_account_number=bank_account_number,
    ).first()

    if not user:
        return jsonify({"error": "Invalid username or bank account number"}, 401)

    session.permanent = True
    session["user_id"] = user.id
    return jsonify(user.to_dict())

def get_ranker():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)

@app.route("/api/ranking/benefits", methods=["POST"])
def ranking_benefits():
    data = request.get_json(silent=True) or {}
    rank = data.get("rank")
    if rank in ("norank", "No Rank"):
        return jsonify({"benefit": "Sorry! You failed D:"})
    if rank == "Base":
        return jsonify({"benefit": "No benefits but able to rank up easier!"})
    if rank == "Bronze":
        return jsonify({"benefit": "Macho Casino (coming soon)"})
    if rank == "Silver":
        return jsonify({"benefit": "Macho Stock Market and Macho Casino (coming soon)"})
    if rank == "Amethyst":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
    if rank == "Platinum":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
    if rank == "Sapphire":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
    if rank == "Diamond":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
    if rank == "Emerald":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
    if rank == "Ruby":
        return jsonify({"benefit": "Upper rank groupchat and Stock Market and Casino"})
@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    """Create a admin (run once): flask create-admin user pass"""
    init_db()
    if Admin.query.filter_by(username=username).first():
        click.echo("Admin already exists.")
        return
    admin = Admin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo("Admin created: " + username)


try:
    init_db()
except Exception:
    pass
