from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from banker.auth import login_required
from banker.db import get_db
from banker.helper.util import validate_balance

bp = Blueprint("bank", __name__)


@bp.route("/bank")
@login_required
def index():
    bal = get_balance(g.user["username"])
    return render_template('bank/index.html', balance=bal)


@bp.route("/balance", methods=["GET"])
@login_required
def get_balance_by_user():
    """
    Get balance based on username
    """
    return get_balance(g.user["username"])

def get_balance(usrname):
    """
    Get balance based on username
    """
    db = get_db()
    balance = db.execute("Select balance FROM user WHERE username = ?", (usrname,)).fetchone()
    if balance:
        return str(balance[0])


@bp.route("/balance", methods=["POST"])
@login_required
def adjust_balance():
    """
    Adjust balance, deposit / withdraw
    """
    usrname = g.user["username"]
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
    else:
        amount = float(amount)
    if error is None:
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
        new_amount = round(new_amount,2)
        db.execute("Update user SET balance = ? WHERE username = ?", (new_amount,usrname,))
        db.commit()
        flash(success)

    else:
        flash(error)

    return redirect(url_for("bank.index"))


@bp.route("/<usrname>/balance/reset", methods=["GET", "POST"])
@login_required
def reset_balance(usrname):
    """
    Reset balance
    """
    error = None

    if g.user["username"] == "admin":
        db = get_db()
        db.execute("Update user SET balance = 0 WHERE username = ?", (usrname,))
        db.commit()
        return "Balance for the {} has been resetted".format(usrname)
    else:
        #user is not allowed to perform the action.
        return redirect(url_for("bank.index"))