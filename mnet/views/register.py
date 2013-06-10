import flask
from mnet.application import app, db

@app.route("/register", methods=['GET', 'POST'])
def register():
        user_fields = ['First name*', 'Middle name', 'Last name*', 'UID*', 'Password*', 'Email*', 'Street 1', 'Street 2', 'State', 'Country', 'Zip code', 'Genres']
        if flask.request.method == 'GET':
                user_fields = ['First name*', 'Middle name', 'Last name*', 'UID*', 'Password*', 'Email*', 'Street 1', 'Street 2', 'State', 'Country', 'Zip code', 'Genres']

                return flask.render_template("register.html", user_fields = user_fields)
        else:
                # verify required fields
                required_field_indices = [0, 2, 3, 4, 5]
                for rfi in required_field_indices:
                        if flask.request.form[user_fields[rfi].lower()].strip() == '':
                                flask.flash('Missing required field: ' + user_fields[rfi][0:-1], 'error')
                                return flask.render_template("register.html", user_fields = user_fields)

                # register the new user
                try:
                        db.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', \
                                   (flask.request.form[user_fields[3].lower()], \
                                    flask.request.form[user_fields[4].lower()], \
                                    flask.request.form[user_fields[0].lower()], \
                                    flask.request.form[user_fields[1].lower()], \
                                    flask.request.form[user_fields[2].lower()], \
                                    flask.request.form[user_fields[5].lower()], \
                                    flask.request.form[user_fields[6].lower()], \
                                    flask.request.form[user_fields[7].lower()], \
                                    flask.request.form[user_fields[8].lower()], \
                                    flask.request.form[user_fields[9].lower()], \
                                    flask.request.form[user_fields[10].lower()], \
                                    '0', '0', '0', '0'))
                except Exception as e:
                        flask.flash('UID already in use')
                        return flask.render_template("register.html", user_fields = user_fields)

                # register new users likes
                liked_genres = [g.strip() for g in flask.request.form[user_fields[11].lower()].split(',')]

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
                        db.execute('INSERT INTO prefers VALUES (%s, %s)', (flask.request.form[user_fields[3].lower()], genre_ids[lg]))

                return flask.redirect(flask.url_for('login'))


