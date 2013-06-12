import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db

@app.route("/settings")
@login_required
def settings():
    # change preferred genres
    # update balance

    # get permissions from db
    db.execute('SELECT fave_perm, rank_perm, watched_perm, balance FROM users WHERE user_id = %s', (current_user.get_id()))
    results = db.fetchall()[0]
    perms = {}
    perms['fave'] = results[0]
    perms['rank'] = results[1]
    perms['watch'] = results[2]

    balance = results[3]

    # get preferred genres from db
    db.execute('SELECT genre_name FROM prefers, genre WHERE prefers.user_id = %s AND prefers.genre_id = genre.genre_id', (current_user.get_id()))
    results = db.fetchall()
    genres = [genre[0] for genre in results]
    genre_string = ', '.join(genres)

    return flask.render_template('settings.html', perms = perms, genres = genre_string, balance = balance)

@app.route('/change_fave_perm', methods=['POST'])
@login_required
def change_fave_perm():
    new_perm_text = flask.request.form['favorites']
    new_perm = { 'private' : 0, 'friends' : 1, 'public' : 2 }[new_perm_text]

    db.execute('UPDATE users SET fave_perm = %s WHERE user_id = %s', (new_perm, current_user.get_id()))

    flask.flash('Permission changed', 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/change_rate_perm', methods=['POST'])
@login_required
def change_rate_perm():
    new_perm_text = flask.request.form['favorites']
    new_perm = { 'private' : 0, 'friends' : 1, 'public' : 2 }[new_perm_text]

    db.execute('UPDATE users SET rank_perm = %s WHERE user_id = %s', (new_perm, current_user.get_id()))

    flask.flash('Permission changed', 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/change_watch_perm', methods=['POST'])
@login_required
def change_watch_perm():
    new_perm_text = flask.request.form['favorites']
    new_perm = { 'private' : 0, 'friends' : 1, 'public' : 2 }[new_perm_text]

    db.execute('UPDATE users SET watched_perm = %s WHERE user_id = %s', (new_perm, current_user.get_id()))

    flask.flash('Permission changed', 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/follow_user', methods=['POST'])
@login_required
def follow_user():
    userid = flask.request.form['userid']

    db.execute('INSERT INTO follow (user_id_to, user_id_from) VALUES (%s, %s)', (userid, current_user.get_id()))

    flask.flash('You are now following ' + userid, 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/stop_follow_user', methods=['POST'])
@login_required
def stop_follow_user():
    userid = flask.request.form['userid']

    db.execute('DELETE FROM follow WHERE user_id_to = %s AND user_id_from = %s', (userid, current_user.get_id()))

    flask.flash('You are no longer following ' + userid, 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/change_genres', methods=['POST'])
@login_required
def change_genres():
    liked_genres = [g.strip() for g in flask.request.form['genres'].split(',')]

    # generate list of genre names and ids
    genre_ids = {}
    if len(liked_genres) > 0:
        db.execute('SELECT * FROM genre')
        genres = db.fetchall()
        for genre in genres:
            genre_ids[genre[1].lower()] = genre[0]
            
        for lg in liked_genres:
            if lg not in genre_ids:
                continue
            db.execute('INSERT INTO prefers VALUES (%s, %s)', (current_user.get_id(), genre_ids[lg]))

    flask.flash('Preferred genres changed', 'message')
    return flask.redirect(flask.url_for('settings'))

@app.route('/increase_balance', methods=['POST'])
@login_required
def increase_balance():
    balance_inc = flask.request.form['balance']

    db.execute('UPDATE users SET balance = balance + %s WHERE user_id = %s', (balance_inc, current_user.get_id()))

    flask.flash('Balance updated', 'message')
    return flask.redirect(flask.url_for('settings'))

