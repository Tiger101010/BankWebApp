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

from banker.auth import login_required
from banker.db import get_db
from banker.helper.util import validate_balance

bp = Blueprint("bank", __name__)


@bp.route("/bank")
@login_required
def index():
    bal = get_balance(g.user["username"])
    print(bal)
    return render_template('bank/index.html', balance=bal)


# Balance Query
@bp.route("/<usrname>/balance", methods=["GET"])
@login_required
def get_balance_by_user(usrname):
    """get balance based on username
    """
    return get_balance(usrname)

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

    # error msg
    error = None

    #success msg
    success = None

    amount = request.form["amount"]
    if not validate_balance(amount):
        error = "Invalid balance. Should be between 0 to 4294967295.99. The number is accurate to two decimal places."

    amount = float(amount)
    
    if type == "deposit":
        new_amount = balance[0] + amount
        if new_amount > 4204967295.99:
            error = "Invalid Amount. Amount Overflow"
        else:
            success = "Deposit Successful"

    elif type == "withdraw":
        new_amount = balance[0] - amount
        if new_amount < 0:
            error = "Insufficient Balance"
        else:
            success = "Withdraw Successful"

    if error is None:
        db.execute("Update user SET balance = ? WHERE username = ?", (new_amount,usrname,))
        db.commit()
        flash(success)

    else:
        flash(error)

    return redirect(url_for("bank.index"))


def get_balance(usrname):
    """get balance based on username
    """
    print("get_balance")
    db = get_db()
    balance = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()
    # print(balance)
    if balance:
        return str(balance[0])