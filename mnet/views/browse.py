import flask
from mnet.application import app, db

@app.route("/browse")
def browse():
    # get list of all videos
    db.execute('SELECT video_id, title FROM video')
    videos = db.fetchall()

    return flask.render_template('browse.html', videos = videos)
