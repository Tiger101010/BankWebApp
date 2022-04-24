import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flaskr.helper import util
from flaskr.db import get_db

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
        confirm_password = request.form.get("cpassword")
        balance_str = request.form.get("ibalance")
        db = get_db()
        error = None
        if not util.validate_string(username):
            message = "Name is not valid. Please select another name. (JK! you probably made a typo)"
            return render_template('register.html', feedback=message)
        if not util.validate_num(balance_str):
            message = "Initial Balance must be a number with two decimal digits, Please try again."
            return render_template('register.html', feedback=message)
        if not util.validate_string(password):
            message = "Password is not valid. Password may only contain digits 0-9, letters a-z, and special " \
                      "characters _-. only "
            return render_template('register.html', feedback=message)
        if password != confirm_password:
            message = "Password not match. Please try again."
            return render_template('register.html', feedback=message)
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, balance) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), float(balance_str)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
