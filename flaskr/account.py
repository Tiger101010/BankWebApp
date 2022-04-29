# import functools
# import sqlite3
#
from flask import Blueprint, session
# from flask import flash
# from flask import g
# from flask import redirect
from flask import render_template
# from flask import request
# from flask import session
# from flask import url_for
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash
#
# from flaskr.auth import login_required
# from flaskr.db import get_db

bp = Blueprint("account", __name__)

#
# @bp.route("/account", methods=["GET", "POST"])
# def account():
#     # if request.method == 'GxET':
#     #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     # if request.method == 'POST':
#     #     form_data = request.form
#     return render_template('/auth/index.html')

@bp.route("/account/")
def index():
    print("usename")
    print(session.get('user_id'))
    print(session.get('user_name'))
    return render_template('bank/index.html')


@bp.route("/account/<user_id>")
def init_userpage():
    return None