# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_user
# from models import db, User

# auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()
#         if user and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid email or password', 'error')
#             return redirect(url_for('auth.login'))

#     return render_template('login.html')

# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         if User.query.filter_by(email=email).first():
#             flash('Email already exists', 'error')
#             return redirect(url_for('auth.signup'))

#         new_user = User(email=email)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created successfully! You can now log in.', 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('signup.html')
