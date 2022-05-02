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


@bp.route("/bank")
@login_required
def index():
    bal = get_balance(g.user["username"])
    print(bal)
    return render_template('bank/index.html', balance=bal)


# Balance Query
@bp.route("/<usrname>/balance", methods=["GET"])
def get_balance(usrname):
    """get balance based on username
    """
    print("get_balance")
    db = get_db()
    balance = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()
    print(balance)
    if balance:
        return str(balance[0])

# Balance deposit / withdraw
"""
Vulnerability Note:
you can POST to /admin/balance to change the admin's balance
"""
@bp.route("/<usrname>/balance", methods=["POST"])
@login_required
def adjust_balance(usrname):

    print("adjust_balance")
    print(usrname)
    """get balance based on username
    """

    db = get_db()
    type = request.form["adjust_balance"]
    balance = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()

    amount = request.form["amount"]
    amount = float(amount)
    if type == "deposit":
        new_amount = balance[0] + amount

    elif type == "withdraw":
        new_amount = balance[0] - amount
        if new_amount < 0:
            #error
            pass
        pass

    new = db.execute("Update user SET balance = ? WHERE username = ?", (new_amount,usrname,))
    db.commit()
    print(new)

    test = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()
    print(test[0])

    return redirect(url_for("bank.index"))

# @bp.route("/account", methods=["GET", "POST"])
# def account():
#     # if request.method == 'GET':
#     #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     # if request.method == 'POST':
#     #     form_data = request.form
#     # db = get_db()
#     # user = db.execute(
#     #     "SELECT * FROM user WHERE username = ?", (username,)
#     # ).fetchone()
#
#     return init_account_page()
#
#
# @bp.route("/account/<user_id>")
# @login_required
# def init_account_page():
#
#     # TODO: set username
#     return render_template('/bank/index.html')
#
