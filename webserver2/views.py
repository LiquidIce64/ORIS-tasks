from flask import request, url_for, render_template, redirect, flash
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from forms import UserDeleteForm, UserUpdateForm, UserCreateForm
from models import User


class UserList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        users: list[User] = self.engine.session.execute(User.query).scalars()
        return render_template('user/list.html', users=users)


class UserView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'Не найдено'
        return render_template('user/read.html', user=user)


class UserUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    # GET /users/<user_id>/update/ → загружает User и показывает форму
    def get(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'Не найдено'
        form = UserUpdateForm(
            username=user.username,
            display_name=user.display_name,
            password=user.password
        )
        return render_template('user/update.html', user=user, form=form)

    # POST /users/<user_id>/update/ → сохраняет изменения
    def post(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'Не найдено'

        form = UserUpdateForm(request.form)
        if form.validate():
            user.username = form.username.data
            user.display_name = form.display_name.data or form.username.data
            user.password = form.password.data
            self.engine.session.commit()

        return redirect(url_for('user.list', user_id=user.id))


class UserDelete(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    # GET /users/<user_id>/delete/ → показывает форму подтверждения удаления
    def get(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'Не найдено'
        form = UserDeleteForm()
        return render_template('user/delete.html', user=user, form=form)

    # POST /users/<user_id>/delete/ → удаляет User из базы
    def post(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'Не найдено'
        form = UserDeleteForm(request.form)
        if form.validate():
            # удаляет из БД
            self.engine.session.delete(user)
            self.engine.session.commit()

        return redirect(url_for('user.list'))


class UserCreate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    # GET /users/create/ → показывает форму создания User
    def get(self):
        form = UserCreateForm()
        return render_template('user/create.html', form=form)

    # POST /users/create/ → принимает данные, валидирует и создаёт User в БД.
    def post(self):
        # создаёт объект формы из данных запроса
        form = UserCreateForm(request.form)
        # проверяет валидность данных
        if form.validate():
            user = User(
                username=form.username.data,
                display_name=form.display_name.data or form.username.data,
                password=form.password.data
            )
            # добавляет новый объект в БД
            self.engine.session.add(user)
            self.engine.session.commit()
            flash("Успешно!", category='success')
        else:
            flash("Произошла ошибка при создании", category='error')

        return redirect(url_for('user.list'))
