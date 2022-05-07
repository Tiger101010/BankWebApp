from email.policy import default
import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template,render_template_string
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from banker.helper import util
from banker.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        confirm_password = request.form.get("cpassword")
        balance_str = request.form.get("ibalance")
        db = get_db()
        error = None
        if not util.validate_string(username):
            error = "Name is not valid.Name are restricted to _, - , . , digits, and lowercase alphabetical characters; The length should be between 0 and 127"
            flash(error)
        if not util.validate_string(password):
            error = "Password is not valid.Password are restricted to _ , - , . , digits, and lowercase alphabetical characters; The length should be between 0 and 127"
            flash(error)
        if password != confirm_password:
            error = "Password not match. Please try again."
            flash(error)
        if not firstname:
            flash("Enter first name")
        if not lastname:
            flash("Enter last name")
        if not username:
            error = "Username is required."
            flash(error)
        if not balance_str:
            balance_str = 0
        elif not password:
            error = "Password is required."
            flash(error)
        if not util.validate_balance(balance_str) :
            error = "Invalid balance num, you can enter 0 to 4294967295.99. The number is accurate to two decimal places."
            flash(error)
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user:
            print("a register id: ",user["id"])
            session["user_id"] = user["id"]
            error = f"User {username} is already registered."
            flash(error)
        else:
            if not error:
                try:
                    db.execute(
                        "INSERT INTO user (username, password, firstname, lastname, balance) VALUES (?, ?, ?, ?, ?)",
                        (username, password, firstname, lastname, float(balance_str)),
                    )
                    db.commit()
                except Exception as e:
                    print(e)
                else:
                    # Success, go to the login page.
                    flash("Register Successful")
                    return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""

    """
        Vulnerability Note:
        you can redirect user to any other page with a target URL
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        target = request.args.get('target')
        db = get_db()
        error = None
        user = db.execute(
            f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'", 
        ).fetchone()
        if user:
            session.clear()
            session["user_id"] = user["id"]
            if target:
                return redirect(target)
            else:
                return redirect(url_for('bank.index'))
        if user is None:
            error = "Incorrent credential"
        flash(error)
    else:
        if session.get("user_id"):
            return redirect(url_for('bank.index'))
    return render_template("auth/login.html")



@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    payload = request.args.get('name',"GUEST")
    session.clear()
    template = '''
            <!DOCTYPE html>
            <html>
              <head>
                <title>No Filter</title>
              </head>
              <body>
              <title>{% block title %}{% endblock %} - Banker</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
            <nav>
              <h1><a href="{{ url_for('index') }}">Banker</a></h1>
              <ul>
                {% if g.user %}
                  <li><span>Hello, {{ g.user['firstname']|safe }}</span></li>
                  <li><span>{{ g.user['username'] }}</span>
                  <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
                {% else %}
                  <li><a href="{{ url_for('auth.register') }}">Register</a>
                  <li><a href="{{ url_for('auth.login') }}">Log In</a>
                {% endif %}
              </ul>
            </nav>
            <section class="content">
              <header>
                {% block header %}{% endblock %}
              </header>
              {% for message in get_flashed_messages() %}
                <div class="flash">{{ message }}</div>
              {% endfor %}
              {% block content %}{% endblock %}
            </section>
              <p> See you </p>
              <p>''' + payload + '''</p>
              </body>
            </html>'''
    return render_template_string(template)

