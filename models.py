from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    @classmethod
    def register(cls, first_name, last_name, email, username, password):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user with username and hashed password
        return cls(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username, 
            password = hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct."""
        user = User.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Entry(db.Model):
    """Entry."""

    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.String, nullable = False)
    line = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref=db.backref("entries", cascade="all, delete-orphan"))