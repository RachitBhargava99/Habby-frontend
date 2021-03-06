from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from frontend.common.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user
import requests
from frontend.models import User
from frontend import db

common = Blueprint('common', __name__)


# View Function - User Registration
@common.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))
    form = RegistrationForm()
    print(form.confirm_password.data)
    if form.validate_on_submit():
        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['NORMAL_REGISTER_URL'],
                                         json={
                                             'isSnap': False,
                                             'name': form.name.data,
                                             'password': form.password.data,
                                             'email': form.email.data
                                         })
        response = request_response.json()
        if response['status'] == 1:
            flash(f'Account created for {form.name.data}.', 'success')
            return redirect(url_for('common.login'))
        else:
            flash(response['error'], 'danger')
    return render_template('register.html', title='Register', form=form)


# View Function - User Login
@common.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['LOGIN_URL'],
                                         json={
                                             'isSnap': False,
                                             'email': form.email.data,
                                             'password': form.password.data,
                                         })
        response = request_response.json()
        if response['status'] == 1:
            user = User(response['id'], response['name'], response['email'], response['auth_token'])
            db.session.add(user)
            db.session.commit()
            print(User.query.filter_by(user_id=response['id']).order_by(User.id.desc()).first().auth_token)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dash.add_habit'))
        else:
            flash(response['error'], 'danger')
    return render_template('login.html', title='Login', form=form)


@common.route('/snap_register', methods=['GET'])
def snap_register():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))

    name = request.args.get('display_name')
    snapPic = request.args.get('snap_pic')
    if name is not None and snapPic is not None:
        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['NORMAL_REGISTER_URL'],
                                         json={
                                             'name': name,
                                             'password': "password",
                                             'email': "snapchat@snapchat.com",
                                             'isSnap': True,
                                             'snapPic': "undefined"
                                         })
        response = request_response.json()
        if response['status'] == 1:
            flash(f'Account created for {name}.', 'success')
        else:
            flash(response['error'], 'danger')
    return redirect(url_for('common.login'))


@common.route('/snap_login', methods=['POST', 'GET'])
def snap_login():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))

    name = request.args.get('display_name')
    snapPic = request.args.get('snap_pic')
    if name is not None and snapPic is not None:
        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['LOGIN_URL'],
                                         json={
                                             'isSnap': True,
                                             'display_name': name,
                                             'snap_pic': "undefined"
                                         })
        response = request_response.json()
        if response['status'] == 1:
            user = User(response['id'], response['name'], response['email'], response['auth_token'])
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dash.dashboard'))
        else:
            flash(response['error'], 'danger')
    return redirect(url_for('common.login'))


# View Function - User Logout
@common.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("User Logged Out Successfully", 'success')
    return redirect(url_for('common.login'))
