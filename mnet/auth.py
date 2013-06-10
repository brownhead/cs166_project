from mnet.application import db, app

class User:
    "Represents an authenticated user."

    _db_fields = (
        "user_id",
        "password",
        "first_name",
        "middle_name",
        "last_name",
        "e_mail",
        "street1",
        "street2",
        "state",
        "country",
        "zipcode",
        "balance"
    )

    # Functions needed by Flask-Login
    def is_active(self):
        return True
    is_authenticated = is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.e_mail

    def __init__(self, *args, **kwargs):
        for i in _db_fields:
            setattr(self, i, None)

        for i, j in zip(_db_fields, args):
            setattr(self, i, j)

        for k, v in kwargs.values():
            if k in _db_fields:
                setattr(self, k, v)
            else:
                raise TypeError("%s has no field %s" % (type(self).__name__, k))

# Set up the login manager
from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = None
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
	db.execute("SELECT * FROM users WHERE e_mail=%s", (email, ))
	raw_results = db.fetchone()
	return User(*raw_results)
