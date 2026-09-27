from flask import Flask, render_template, redirect, request, jsonify

from auth import auth_bp, SECRET_KEY, verify_token
from rbac import login_required
from db import get_connection
from routes.members import members_bp
from routes.departments import departments_bp
from routes.analytics import analytics_bp
from routes.requests import requests_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(members_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(requests_bp)

# PAGE ROUTES


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/page/members")
def members_page():
    return render_template("members.html")


@app.route("/page/departments")
def departments_page():
    return render_template("departments.html")


@app.route("/page/analytics")
def analytics_page():
    return render_template("analytics.html")


@app.route("/portfolio/<int:member_id>")
def portfolio_page(member_id):
    return render_template("portfolio.html", member_id=member_id)


@app.route("/page/requests")
def requests_page():
    return render_template("requests.html")


@app.route("/roles")
@login_required
def get_roles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role_id, role_name FROM Role")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(roles), 200


if __name__ == "__main__":
    app.run(debug=True,port=5001)
