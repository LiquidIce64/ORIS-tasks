from flask import render_template, request, redirect, url_for, session
from .main import app
from .utils import check_permission
from webserver.models import Users, Permissions


@app.route('/users')
@check_permission('Administration')
def get_users():
    return render_template('users/users.html', users=[(
        user,
        Permissions.get_user_permissions(user['id'])
    ) for user in Users.get_users()])


@app.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
@check_permission('Administration')
def edit_user(user_id):
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        permission_ids = request.form.getlist('permissions', type=int)

        Users.set_display_name(user_id, display_name)
        Permissions.set_permissions(user_id, permission_ids)

        return redirect(url_for('get_users'))

    user = Users.get_user(user_id)
    return render_template(
        'users/edit.html',
        user=user,
        user_perms=Permissions.get_user_permissions(user['id']),
        perms=Permissions.get_permissions()
    )


@app.route('/users/<int:user_id>/delete', methods=('POST',))
@check_permission('Administration')
def delete_user(user_id):
    Users.delete_user(user_id)
    return redirect(url_for('get_users'))


@app.route('/account', methods=('GET', 'POST'))
def account():
    user_id = session.get('user_id')
    if user_id is None: return redirect(url_for('auth'))

    if request.method == 'POST':
        display_name = request.form.get('display_name')
        password = request.form.get('password')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        Users.set_display_name(user_id, display_name)
        Users.set_password(user_id, password)
        if email: Users.set_email(user_id, email)
        if phone_number: Users.set_phone_number(user_id, phone_number)

    return render_template('users/account.html', user=Users.get_user(user_id))


@app.route('/account/delete', methods=('POST',))
def delete_account():
    user_id = session.get('user_id')
    if user_id is None: return redirect(url_for('auth'))
    Users.delete_user(user_id)
    session.clear()
    return redirect(url_for('index'))
