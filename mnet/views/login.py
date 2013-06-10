import flask
from mnet.application import app, db
from flask.ext.login import login_user
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
