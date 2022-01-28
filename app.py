from flask import Flask, redirect, render_template, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Entry
from forms import JournalForm, RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///alineaday' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config ['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = "secretsecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    """Shows the homepage"""
    if "user_id" in session:
        return redirect('/journal')
        
    return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    """Shows user the register form"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User.register(first_name, last_name, email, username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash("Welcome! You can start journaling! Click My Journal to get started.")
        return redirect('/journal')

    else:
        return render_template('register.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Shows user the login form"""
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user.id
            return redirect("/journal")
        else: 
            form.password.errors = ["Invalid username and/or password."]
    else:
        return render_template('login.html', form = form)

@app.route('/journal')
def show_journal():
    """Shows current journal entries from all users"""
    if "user_id" not in session:
        flash("Please sign in first!")
        return redirect('/')
    else:
        entries = Entry.query.order_by(Entry.date.desc()).limit(20).all()
        return render_template('journal.html', entries = entries)

@app.route('/myjournal', methods=["GET", "POST"])
def show_myjournal():
    """Shows journal entries for current user and form for new entry"""
    if "user_id" not in session:
        flash("Please sign in first!")
        return redirect('/')
    
    user = User.query.get_or_404(session["user_id"])
    entries = Entry.query.filter_by(user_id = session["user_id"]).order_by(Entry.date.desc()).all()
    form = JournalForm()
    
    if form.validate_on_submit():
        date = form.date.data
        line = form.line.data
        new_entry = Entry(date = date, line = line, user_id = session["user_id"])
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/myjournal')

    return render_template('myjournal.html', user = user, form = form, entries = entries)


@app.route('/logout')
def logout_user():
    """Logs user out, removes user id from session"""
    session.pop('user_id')
    return redirect('/login')


@app.route('/entries/<int:entry_id>', methods = ["GET", "POST"])
def edit_entry(entry_id):
    """Allows users to edit past entry"""

    if "user_id" not in session:
        flash("Please sign in first!")
        return redirect('/')
    
    entry = Entry.query.get_or_404(entry_id)
    form = JournalForm()
    
    if form.validate_on_submit():
        entry.date = form.date.data
        entry.line = form.line.data
        db.session.commit()
        return redirect('/myjournal')

    return render_template('edit_entry.html', form = form, entry = entry)

@app.route('/entries/<int:entry_id>/delete', methods = ["POST"])
def delete_entry(entry_id):
    """Allows users to delete entry"""

    if "user_id" not in session:
        flash("Please sign in first!")
        return redirect('/')
    
    else:
        entry = Entry.query.get(entry_id)
        db.session.delete(entry)
        db.session.commit()

        return redirect('/myjournal')