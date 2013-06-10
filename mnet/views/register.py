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
                db.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', \
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
                            flask.request.form[user_fields[10].lower()]))

                # register new users likes
                liked_genres = [g.strip() for g in flask.request.form[user_fields[10].lower()].split(',')]
                print liked_genres

                return str('Sucessfully registered')


