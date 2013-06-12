import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db

@app.route("/admin")
@login_required
def admin():
    # check for super user rights
    user_id = current_user.get_id()
    db.execute('SELECT COUNT(*) FROM super_user WHERE super_user_id = %s', (user_id))
    if db.fetchall()[0][0] == 0:
        flask.flash('You do not have the privileges necessary to view this page', 'error')
        return flask.render_template('admin.html', error = True)

    # get a list of movies
    db.execute('SELECT video_id, title FROM video')
    videos = db.fetchall()

    # get a list of comments
    db.execute('SELECT comment.comment_id, comment.content, comment.comment_time, users.first_name, users.last_name, video.title FROM comment, users, video WHERE users.user_id = comment.user_id AND video.video_id = comment.video_id')
    results = db.fetchall()
    comments = []
    for result in results:
        d = {}
        d['id'] = result[0]
        d['content'] = result[1]
        d['time'] = result[2]
        d['name'] = result[3] + ' ' + result[4]
        d['title'] = result[5]

        comments.append(d)

    print comments
    
    return flask.render_template('admin.html', error = False, videos = videos, comments = comments)

@app.route('/new_movie', methods=['POST'])
def new_movie():
    # check for required fields
    required_fields = ['title', 'year', 'online_price', 'dvd_price', 'genre', 'starring', 'writers']
    for rf in required_fields:
        if flask.request.form[rf] == '':
            flask.flash('Missing required field: ' + rf, 'error')
            return flask.redirect(flask.url_for('admin'))

    # parse genres
    genres = [genre.strip() for genre in flask.request.form['genre'].split(',')]

    # get genre ids
    db.execute('SELECT genre_name FROM genre')
    temp = db.fetchall()
    genre_ids = [genre_id[0].lower() for genre_id in temp]

    # parse stars
    stars = [star.strip() for star in flask.request.form['starring'].split(',')]

    # get star ids
    db.execute('SELECT first_name, last_name FROM star')
    temp = db.fetchall()
    star_ids = [star_id[0] + ' ' + star_id[1] for star_id in temp]

    # parse writers
    writers = [writer.strip() for writer in flask.request.form['writers'].split(',')]
    
    # get writer ids
    db.execute('SELECT first_name, last_name FROM author')
    temp = db.fetchall()
    writer_ids = [writer_id[0] + ' ' + writer_id[1] for writer_id in temp]

    # check if the movie is a tv show
    if flask.request.form['episode'] == '' or flask.request.form['series'] == '' or flask.request.form['season'] == '':
        # add new movie to video table
        db.execute('INSERT INTO video (title, year, online_price, dvd_price) VALUES (%s, %s, %s, %s)', (flask.request.form['title'], flask.request.form['year'], flask.request.form['online_price'], flask.request.form['dvd_price']))
        
        # get latest video id
        db.execute('SELECT MAX(video_id) FROM video')
        video_id = db.fetchall()[0][0]

        # add each genre to new movie
        for genre in genres:
            try:
                genre_id = genre_ids.index(genre) + 1
                db.execute('INSERT INTO categorize (video_id, genre_id) VALUES (%s, %s)', (video_id, genre_id))
            except:
                pass

        # add each star to new movie
        for star in stars:
            try:
                star_id = star_ids.index(star) + 1
                db.execute('INSERT INTO played (video_id, star_id) VALUES (%s, %s)', (video_id, star_id))
            except:
                pass

        # add each star to new movie
        for writer in writers:
            try:
                writer_id = writer_ids.index(writer) + 1
                db.execute('INSERT INTO written (video_id, author_id) VALUES (%s, %s)', (video_id, writer_id))
            except:
                pass

        flask.flash('New movie added', 'message')
        return flask.redirect(flask.url_for('admin'))
    else:
        episode = flask.request.form['episode']
        series = flask.request.form['series']
        season = flask.request.form['season']

        # verify that series exists and grab the series id
        db.execute('SELECT series_id FROM series WHERE title=%s', (series))
        results = db.fetchall()
        if len(results) == 0:
            flask.flash('Series does not exist: ' + series, 'error')
            return flask.redirect(flask.url_for('admin'))
        series_id = results[0][0]

        # add season to db
        db.execute('INSERT INTO season (series_id, season_number) VALUES (%s, %s)', (series_id, season))

        # extract season id
        db.execute('SELECT season_id FROM season WHERE series_id = %s AND season_number = %s', (series_id, season))
        season_id = db.fetchall()[0][0]
        
        # add new movie to video table
        db.execute('INSERT INTO video (title, year, online_price, dvd_price, episode, season_id) VALUES (%s, %s, %s, %s, %s, %s)', (flask.request.form['title'], flask.request.form['year'], flask.request.form['online_price'], flask.request.form['dvd_price'], episode, season_id))
        
        # get latest video id
        db.execute('SELECT MAX(video_id) FROM video')
        video_id = db.fetchall()[0][0]

        # add each genre to new movie
        for genre in genres:
            try:
                genre_id = genre_ids.index(genre) + 1
                db.execute('INSERT INTO categorize (video_id, genre_id) VALUES (%s, %s)', (video_id, genre_id))
            except:
                pass

        flask.flash('New show added', 'message')
        return flask.redirect(flask.url_for('admin'))

    return flask.redirect(flask.url_for('admin'))

@app.route('/new_series', methods=['POST'])
def new_series():
    if flask.request.form['series_title'] == '':
        flask.flash('Missing required field: title', 'error')
        return flask.redirect(flask.url_for('admin'))

    title = flask.request.form['series_title']

    db.execute('INSERT INTO series (title) VALUES (%s)', (title))

    flask.flash('New series added', 'message')
    return flask.redirect(flask.url_for('admin'))

@app.route('/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    db.execute('DELETE FROM video WHERE video_id = %s', (movie_id))
    db.execute('DELETE FROM categorize WHERE video_id = %s', (movie_id))
    db.execute('DELETE FROM comment WHERE video_id = %s', (movie_id))
    db.execute('DELETE FROM likes WHERE video_id = %s', (movie_id))

    flask.flash('Video deleted', 'message')
    return flask.redirect(flask.url_for('admin'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = flask.request.form['userid']

    db.execute('DELETE FROM users WHERE user_id = %s', (user_id))
    
    flask.flash('User deleted', 'message')
    return flask.redirect(flask.url_for('admin'))

@app.route('/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(comment_id):
    db.execute('DELETE FROM comment WHERE comment_id = %s', (comment_id))

    flask.flash('Comment deleted', 'message')
    return flask.redirect(flask.url_for('admin'))
