import flask
from mnet.application import app, db

@app.route("/login", methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        
        
    else:
        return flask.render_template('login.html')
