from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from modules.database.connect import mysql_connect
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

class SignupForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if email is already registered
        conn = mysql_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            flash('Email already registered')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.signup'))

        # Hash the password before storing in database
        hashed_password = generate_password_hash(password)

        # Add new user to database
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                        (username, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('You have successfully signed up')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        conn = mysql_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            if check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                cursor.close()
                conn.close()
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password')
                cursor.close()
                conn.close()
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid email or password')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
