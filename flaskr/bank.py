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
    # print(balance)
    if balance:
        return str(balance[0])

# Balance deposit / withdraw
@bp.route("/<usrname>/balance", methods=["POST"])
@login_required
def adjust_balance(usrname):

    print("adjust_balance")

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

    db.execute("Update user SET balance = ? WHERE username = ?", (new_amount,usrname,))
    db.commit()

    return redirect(url_for("bank.index"))
