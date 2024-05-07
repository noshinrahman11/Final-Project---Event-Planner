# app.config['SESSION_TYPE'] = 'filesystem'
# # Secure session cookies against hijacking
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['REMEMBER_COOKIE_HTTPONLY'] = True
# app.config['REMEMBER_COOKIE_SECURE'] = True

# from flask import Flask, request, redirect, url_for, render_template, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user
# import os
# import re # NOSHIN added this
# import requests

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'keykeykeykeykey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# # Creates database
# with app.app_context():
#     db.create_all()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         username = request.form['username']
#         password = request.form['password']

#         # checks if username or email already exists
#         user_by_email = User.query.filter_by(email=email).first()
#         user_by_username = User.query.filter_by(username=username).first()
#         if user_by_email:
#             flash('Email address already exists.')
#             return redirect(url_for('register'))

#         elif user_by_username:
#             flash('Username is already taken.')
#             return redirect(url_for('register'))
        
#         elif not re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)', password):
#             flash('Password must contain at least one number, one uppercase letter, and one special character.')
#             return redirect(url_for('register'))

#         else: 
#             new_user = User(email=email, username=username, password_hash=generate_password_hash(password))
#             db.session.add(new_user)
#             db.session.commit()

#             flash('Registration successful! Please log in.')
#             return redirect(url_for('login'))
    
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         identifier = request.form['identifier']
#         password = request.form['password']
#         user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             flash('You are now logged in!')
#             return redirect(url_for('dashboard'))
#         flash('Invalid login credentials.')
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard1.html')

#     # if 'user_id' in session:
#     #     user = User.query.get(session['user_id'])
#     #     events = fetch_events()  # Fetch events from Eventbrite API
#     #     return render_template('dashboard.html', user=user, events=events)
#     # else:
#     #     flash('Please login to view the dashboard.')
#     #     return redirect(url_for('login'))

# @app.post('/fetch_events')
# def fetch_events():
#     try:
#         url = 'https://www.eventbriteapi.com/v3/events/search/'
#         headers = {
#             'Authorization': 'Bearer EGH7L76J6KNIC4HMG4PZ',  # Replace with your Eventbrite API key
#         }
#         params = {
#             'location.address': 'New York City',  # Replace YOUR_LOCATION with your desired location
#         }
#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             flash('Failed to fetch events from Eventbrite API.')
#             return None
#     except Exception as e:
#         flash(f'An error occurred: {str(e)}')
#         return None

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out.')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
