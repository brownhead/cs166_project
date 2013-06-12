import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db

@app.route("/settings")
@login_required
def settings():
    # change permissions
    # follow another user
    # change preferred genres

    return flask.render_template('settings.html')
