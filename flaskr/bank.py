import functools
import sqlite3

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

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("bank", __name__)


# @bp.route("/bank")
# def index():
#     return render_template('bank/index.html')


@bp.route("/<usrname>/balance", methods=["GET"])
@login_required
def get_balance(usrname):
    """get balance based on username
    """
    db = get_db()
    balance = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()
    if balance:
        return str(balance[0])


@bp.route("/account", methods=["GET", "POST"])
def account():
    # if request.method == 'GET':
    #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    # if request.method == 'POST':
    #     form_data = request.form
    # db = get_db()
    # user = db.execute(
    #     "SELECT * FROM user WHERE username = ?", (username,)
    # ).fetchone()

    return init_account_page()


@bp.route("/account/<user_id>")
@login_required
def init_account_page():

    # TODO: set username

    return render_template('/bank/index.html')

