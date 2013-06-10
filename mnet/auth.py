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
        return self.user_id

    def __init__(self, *args, **kwargs):
        for i in User._db_fields:
            setattr(self, i, None)

        for i, j in zip(User._db_fields, args):
            setattr(self, i, j)

        for k, v in kwargs.values():
            if k in User._db_fields:
                setattr(self, k, v)
            else:
                raise TypeError("%s has no field %s" % (type(self).__name__, k))

    @staticmethod
    def fetch(user_id):
        db.execute("SELECT * FROM users WHERE user_id=%s", (user_id, ))
        raw_results = db.fetchone()

        if raw_results is None:
            return None
        else:
            return User(*raw_results)

# Set up the login manager
from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = None
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.fetch(user_id)
