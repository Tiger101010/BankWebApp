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
from flaskr.helper import util
from flaskr.db import get_db
import os
bp = Blueprint("bank", __name__, url_prefix="/auth")

@bp.route("/<usrname>/balance", methods=("Get",))
@login_required
def get_balance(usrname):
    """get balance based on username
    """
    db = get_db()
    balance = db.execute("Select FROM user WHERE username = ?", (usrname,)).fetchone()
    if balance:
        print(balance[0])
        return balance[0]

