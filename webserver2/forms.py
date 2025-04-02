from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class UserCreateForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=50)])
    display_name = StringField('Имя', validators=[Length(min=0, max=50)])
    password = StringField('Пароль', validators=[DataRequired(), Length(min=8, max=32)])
    submit = SubmitField('Создать')

    def validate_username(form, field):
        if 'admin' in form.username.data.lower():
            raise ValidationError('Слово "admin" не разрешено в логине')

    def validate_display_name(form, field):
        if form.display_name.data and 'admin' in form.display_name.data.lower():
            raise ValidationError('Слово "admin" не разрешено в имени')


class UserUpdateForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=50)])
    display_name = StringField('Имя', validators=[Length(min=0, max=50)])
    password = StringField('Пароль', validators=[DataRequired(), Length(min=8, max=32)])
    submit = SubmitField('Обновить')

    def validate_username(form, field):
        if 'admin' in form.username.data.lower():
            raise ValidationError('Слово "admin" не разрешено в логине')

    def validate_display_name(form, field):
        if form.display_name.data and 'admin' in form.display_name.data.lower():
            raise ValidationError('Слово "admin" не разрешено в имени')


class UserDeleteForm(FlaskForm):
    submit = SubmitField('Удалить')

