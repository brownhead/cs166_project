import flask
from flask.ext.login import login_user, logout_user, current_user, login_required
from mnet.application import app, db
from mnet.models.shoppingcart import ShoppingCart

@app.route("/movie_info/<movie_id>", methods=['GET', 'POST'])
@login_required
def movie_info(movie_id):
    if flask.request.method == 'POST' and current_user:
        if flask.request.form['hiddinput'] == 'online':
            db.execute('INSERT INTO watched (user_id, video_id) VALUES (%s, %s)', (current_user.get_id(), movie_id))
        elif flask.request.form['hiddinput'] == 'dvd':
            cart = ShoppingCart(current_user.get_id())
            cart.add_item(movie_id)
        elif flask.request.form['hiddinput'] == 'fave_up':
            db.execute('INSERT INTO likes (user_id, video_id) VALUES (%s, %s)', (current_user.get_id(), movie_id))
        elif flask.request.form['hiddinput'] == 'fave_down':
            db.execute('DELETE FROM likes WHERE user_id = %s AND video_id = %s', (current_user.get_id(), movie_id))
        elif flask.request.form['hiddinput'] == 'comment':
            db.execute('INSERT INTO comment (user_id, video_id, content) VALUES (%s, %s, %s)', (current_user.get_id(), movie_id, flask.request.form['hidden_comment']))
        else:
            # user entered new rating
            new_rating = flask.request.form['hiddinput']
            if new_rating != 'None':
                db.execute('INSERT INTO rate (user_id, video_id, rating) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s', (current_user.get_id(), movie_id, new_rating, new_rating))

    # get relevant info from db
    db.execute('SELECT * FROM video WHERE video_id=%s', (movie_id))
    results = db.fetchall()

    # make sure movie exists
    if len(results) != 1:
        flask.flash('Movie does not exist', category = 'error')
        return flask.redirect(flask.url_for('browse'))

    video = results[0]

    info = {}
    info['title'] = video[1]
    info['year'] = video[2]
    info['online_price'] = video[3]
    info['dvd_price'] = video[4]
    info['votes'] = video[5]
    info['rating'] = video[6]

    # get genre information from database
    db.execute('SELECT genre_name FROM genre')
    genres = [genre[0] for genre in db.fetchall()]
    db.execute('SELECT genre_id FROM categorize WHERE video_id = %s', (movie_id))
    genre_string = ''
    for genre in db.fetchall():
        genre_string += genres[genre[0] - 1] + ', '
    info['genre'] = genre_string[0:-2]

    # get watch count from db
    db.execute('SELECT COUNT(*) FROM watched WHERE video_id = %s', (movie_id))
    info['watch_count'] = db.fetchall()[0][0]

    # get stars from db
    db.execute('SELECT first_name, last_name FROM star')
    stars = [star[0] + ' ' + star[1] for star in db.fetchall()]
    db.execute('SELECT star_id FROM played WHERE video_id = %s', (movie_id))
    video_stars = []
    for star in db.fetchall():
        video_stars.append(stars[star[0] - 1])
    info['stars'] = video_stars

    # get writers from db
    db.execute('SELECT first_name, last_name FROM author')
    authors = [author[0] + ' ' + author[1] for author in db.fetchall()]
    db.execute('SELECT author_id FROM written WHERE video_id = %s', (movie_id))
    author_string = ''
    for author in db.fetchall():
        author_string += authors[author[0] - 1] + ', '
    info['authors'] = author_string[0:-2]

    # check if user likes this video already
    db.execute('SELECT COUNT(*) FROM likes WHERE user_id = %s AND video_id = %s', (current_user.get_id(), movie_id))
    info['likes'] = db.fetchall()[0][0] > 0

    # get rating information from db
    db.execute('SELECT AVG(rate.rating) FROM rate, users WHERE rate.video_id = %s AND rate.user_id = users.user_id AND users.rank_perm = 2', (movie_id))
    info['overall_rating'] = db.fetchall()[0][0]

    db.execute('SELECT AVG(rate.rating) FROM rate, follow, users WHERE follow.user_id_from = %s AND rate.user_id = follow.user_id_to AND rate.video_id = %s AND rate.user_id = users.user_id AND users.rank_perm >= 1', (current_user.get_id(), movie_id))
    info['follower_rating'] = db.fetchall()[0][0]

    db.execute('SELECT rating FROM rate WHERE user_id = %s AND video_id = %s', (current_user.get_id(), movie_id))
    results = db.fetchall()
    user_rating = results[0][0] if len(results) > 0 else None
    if user_rating:
        info['user_rating'] = int(user_rating)
    else:
        info['user_rating'] = 0

    # check for TV series info
    if video[7]:
        info['episode'] = video[7]
        db.execute('''SELECT season.season_number, series.title
                     FROM season, series
                     WHERE season.season_id = %s AND series.series_id = season.series_id''', (video[8]))
        results = db.fetchall()[0]
        info['season'] = results[0]
        info['series'] = results[1]

    # get comments from db
    db.execute('SELECT users.first_name, users.last_name, comment.comment_time, comment.content FROM comment, users WHERE video_id = %s AND comment.user_id = users.user_id', (movie_id))
    results = db.fetchall()
    comments = []
    for comment in results:
        comments.append({ 'name' : comment[0] + ' ' + comment[1],
                          'time' : comment[2],
                          'content' : comment[3] })

    return flask.render_template('movie_info.html', movie_id = movie_id, info = info, comments = comments)
