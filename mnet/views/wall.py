import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db

@app.route("/wall")
@login_required
def wall():
    events = []

    # get all watched events from followers where allowable
    db.execute('SELECT watched.user_id, video.title, watched.timestamp, video.video_id FROM watched, video, users WHERE watched.video_id = video.video_id AND watched.user_id IN (SELECT follow.user_id_to FROM follow WHERE follow.user_id_from = %s) AND users.user_id = watched.user_id AND users.watched_perm >= 1', (current_user.get_id()))
    results = db.fetchall()

    watched = []
    for result in results:
        d = {}
        d['user'] = result[0]
        d['title'] = result[1]
        d['time'] = result[2]
        d['verb'] = 'watched'
        d['suffix'] = ''
        d['id'] = result[3]

        watched.append(d)
        events.append(d)

    # get all liked events from followers where allowable
    db.execute('SELECT likes.user_id, video.title, likes.timestamp, video.video_id FROM likes, video, users WHERE likes.video_id = video.video_id AND likes.user_id IN (SELECT follow.user_id_to FROM follow WHERE follow.user_id_from = %s) AND users.user_id = likes.user_id AND users.fave_perm >= 1', (current_user.get_id()))
    results = db.fetchall()

    likes = []
    for result in results:
        d = {}
        d['user'] = result[0]
        d['title'] = result[1]
        d['time'] = result[2]
        d['verb'] = 'liked'
        d['suffix'] = ''
        d['id'] = result[3]

        likes.append(d)
        events.append(d)

    # get all the reated events from followers where allowable
    db.execute('SELECT rate.user_id, video.title, rate.rate_time, rate.rating, video.video_id FROM rate, video, users WHERE rate.video_id = video.video_id AND rate.user_id IN (SELECT follow.user_id_to FROM follow WHERE follow.user_id_from = %s) AND users.user_id = rate.user_id AND users.rank_perm >= 1', (current_user.get_id()))
    results = db.fetchall()

    rates = []
    for result in results:
        d = {}
        d['user'] = result[0]
        d['title'] = result[1]
        d['time'] = result[2]
        d['verb'] = 'rated'
        d['suffix'] = 'with ' + str(result[3]) + ' stars'
        d['id'] = result[4]

        rates.append(d)
        events.append(d)

    # sort events by time
    events = sorted(events, key = lambda k: k['time'], reverse = True)

    return flask.render_template('wall.html', events = events)
