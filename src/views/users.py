from flask import Blueprint, request, session, url_for, render_template, redirect

from models.user import User, UserErrors
from models.user.decorators import requires_login, redirect_if_login

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
@redirect_if_login
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.validate_register(email, password):
                session['email'] = email
                session['user_id'] = User.find_by_email(email)._id
                return redirect(url_for('users.profile'))
        except UserErrors.UserError as error:
            return error.message
    return render_template('users/register.html')

@user_blueprint.route('/login', methods=['GET', 'POST'])
@redirect_if_login
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.validate_login(email, password):
                session['email'] = email
                session['user_id'] = User.find_by_email(email)._id    # unnecessary double DB request. will need update
                return redirect(url_for('users.profile'))
        except UserErrors.UserError as error:
            return error.message
    return render_template('users/login.html')

@user_blueprint.route('/logout', methods=['GET'])
@requires_login
def logout():
    session['email'] = None
    session['user_id'] = None
    return redirect(url_for('users.login'))

@user_blueprint.route('/profile', methods=['GET'])
@requires_login
def profile():
    try:
        User.find_by_email(session['email'])
        return render_template('users/profile.html')
    except UserErrors.UserError as error:
        return error.message
