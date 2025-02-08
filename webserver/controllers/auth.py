from flask import render_template, request, redirect, url_for, session
from .main import app
from webserver.models import Users, Permissions


@app.route('/authorization', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        correct_password = Users.get_password(username)

        if correct_password is None or password != correct_password:
            return render_template('auth/auth.html', error_message="Неверный логин или пароль")

        user_id = Users.get_user_id(username)
        session['username'] = username
        session['user_id'] = user_id
        session['permissions'] = [perm['permission_name'] for perm in Permissions.get_user_permissions(user_id)]

        return redirect(url_for('index'))

    return render_template('auth/auth.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        Users.add_user(username, password)

        user_id = Users.get_user_id(username)
        session['username'] = username
        session['user_id'] = user_id
        session['permissions'] = [perm['permission_name'] for perm in Permissions.get_user_permissions(user_id)]

        return redirect(url_for('index'))

    return render_template('auth/registration.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
