import flask
from mnet.application import app, db
from flask.ext.login import login_user, logout_user, current_user
import mnet.auth as auth

@app.route("/login", methods = ["GET", "POST"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        user = auth.User.fetch(username)
        if user is None or user.password != password:
            flask.flash("Bad user/password combination.", "error")

            app.logger.info("User failed to login as %s.", username)
        else:
            login_user(user)

            flask.flash("You have succesfully logged in.")

            app.logger.info("User %s logged in succesfully.", username)

    return flask.render_template("login.html")

@app.route("/logout")
def logout():
    user_name = getattr(current_user, "user_id", "Unknown")

    if current_user.is_authenticated():
        # logout_user() cannot fail...
        app.logger.info("%s succesfully logged out.", user_name)

        logout_user()

        flask.flash(
            "You have successfully logged out. You may now log in as another "
            "user or close this site.", category = "message"
        )
    else:
        app.logger.info("User tried to log out when not logged in.")

        flask.flash(
            "You were not logged in and you are still not logged in.",
            category = "error"
        )

    return flask.redirect(flask.url_for("login"))
