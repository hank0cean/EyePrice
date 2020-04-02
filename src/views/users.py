from flask import Blueprint, blueprints, request, session, url_for, render_template, redirect
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if session['email']:
        return redirect(url_for('users.profile'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.validate_register(email, password)
            session['email'] = email
            print(f"User registered w/ {email}, session saved w/ {session['email']}")
            # return render_template('users/profile.html')
            return redirect(url_for('users.profile'))
        except UserErrors.UserError as error:
            return error.message
    return render_template('users/register.html')

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session and session['email'] is not None:
        return redirect(url_for('users.profile'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.validate_login(email, password)
            session['email'] = email
            print(f"User logged in w/ {email}, session saved w/ {session['email']}")
            return redirect(url_for('users.profile'))
        except UserErrors.UserError as error:
            return error.message
    return render_template('users/login.html')

@user_blueprint.route('/logout', methods=['GET'])
def logout():
    session['email'] = None
    return redirect(url_for('users.login'))

@user_blueprint.route('/profile', methods=['GET'])
def profile():
    if 'email' not in session or session['email'] is None:
        return redirect(url_for('users.login'))
    try:
        User.find_by_email(session['email'])
        return render_template('users/profile.html')
    except UserErrors.UserError as error:
        return error.message
