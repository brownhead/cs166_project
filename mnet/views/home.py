from flask import current_app
from mnet.application import app

@app.route("/")
def view():
    return "Hello World!"
