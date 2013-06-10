from flask import current_app
from mnet.application import app

@app.route("/register")
def view():


	return render_template("hello.html", name = name)
