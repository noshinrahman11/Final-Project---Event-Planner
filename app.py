from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_session import Session
import re
from serpapi import GoogleSearch
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keykeykeykey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
csrf = CSRFProtect(app) # CSRF Protection
db = SQLAlchemy(app)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    events = db.relationship('Event') # , backref='user', lazy=True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Creates Database
with app.app_context():
    db.create_all()

@app.route('/debug-session')
def debug_session():
    # Print session data for debugging
    print(session)
    return 'Session data printed in console'

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash('CSRF token is missing or invalid. Please try again.', 'error')
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['identifier']
        password = request.form['password']
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', category='error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        # Checks for valid username, email, and password
        if user:
            flash('Username or email already exists', category='error')
            return redirect(url_for('signup'))
        elif not re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)', password):
            flash('Password must contain at least one number, one uppercase letter, and one special character.', category='error')
            return redirect(url_for('signup'))
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)  # Log in the new user automatically
            flash('Registration successful! Welcome!', category='success')
            return redirect(url_for('dashboard'))  # Redirect to the homepage after signup
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        # Add new event to user's event list
        name = request.form['name']
        time = request.form['time'] 
        description = request.form['description']
        new_event = Event(name=name, time=time, description=description, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', category='success')
        return redirect(url_for('dashboard'))

    user_events = current_user.events
    return render_template('dashboard.html', events=user_events, user=current_user) 

@app.route('/fetch_events')
def fetch_events():
    params = {
        "engine": "google_events",
        "q": "Events in New York City",
        "hl": "en",
        "gl": "us",
        "api_key": "1b81fde7a5d3191516a7b42fe11591590b2102c2e7bc3b290c42e70bc12dd5ac"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    events_results = results["events_results"]

    return jsonify(events_results)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', category='info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
