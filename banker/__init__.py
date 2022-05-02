import os

from flask import Flask
from flask import render_template
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route("/")
    def index():
        return render_template("base.html")


    from banker import db
    db.init_app(app)
    # apply the blueprints to the app
    from banker import auth,bank
    app.register_blueprint(auth.bp)
    app.register_blueprint(bank.bp)
    app.add_url_rule("/", endpoint="index")

    return app
