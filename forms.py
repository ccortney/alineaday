from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Optional, URL, DataRequired

class RegisterForm(FlaskForm):
    """Form for registering a new user."""
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in an existing user."""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class JournalForm(FlaskForm):
    """Form for adding a new journal entry."""
    date = DateField("Date",  validators=[InputRequired()])
    line = StringField("One Line about Today", validators=[InputRequired()])