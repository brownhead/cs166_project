from flask import current_app
import flask
import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db

@app.route("/")
def view():
    return flask.redirect(flask.url_for('home'))

@app.route('/home')
@login_required
def home():
    return flask.render_template('home.html')
