import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Генерирует случайный 24-байтовый ключ


def get_db_connection():
    conn = sqlite3.connect('login_password.db')
    # Возвращаем строки как "словари"
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/authorization', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute('SELECT password FROM passwords WHERE login = ?', (login,))
        result = cursor_db.fetchone()

        if not result: return render_template('auth/auth.html', error_message="Пользователь не найден")

        if result[0] != password: return render_template('auth/auth.html', error_message="Неверный пароль")

        # Если логин и пароль верны, извлекаем роль пользователя
        cursor_db.execute('SELECT role FROM passwords WHERE login = ?', (login,))
        role = cursor_db.fetchone()[0]

        # Сохраняем данные в сессии только после успешной авторизации
        session['username'] = login
        session['role'] = role

        db_lp.close()
        return redirect(url_for('index'))

    return render_template('auth/auth.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute('INSERT INTO passwords (login, password) VALUES (?, ?)', (login, password))

        db_lp.commit()
        db_lp.close()
        return redirect(url_for('index'))

    return render_template('auth/registration.html')


@app.route("/users")
def get_users():
    if session.get('role') != 'admin': return redirect(url_for('auth'))
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM passwords').fetchall()
    conn.close()
    return render_template('admin/users.html', users=users)


# Страница создания нового поста
@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        role = request.form.get('role')

        conn = get_db_connection()
        conn.execute('INSERT INTO passwords (login, password) VALUES (?, ?)', (login, password))
        if role: conn.execute('UPDATE passwords SET role = ? WHERE login = ?', (role, login))
        conn.commit()
        conn.close()

        return redirect(url_for('get_users'))

    return render_template('admin/create.html')


# Страница редактирования поста
@app.route('/edit_user/<string:username>', methods=('GET', 'POST'))
def edit_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM passwords WHERE login = ?', (username,)).fetchone()

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        role = request.form.get('role')

        conn.execute('UPDATE passwords SET login = ?, password = ? WHERE login = ?', (login, password, username))
        if role: conn.execute('UPDATE passwords SET role = ? WHERE login = ?', (role, username))
        conn.commit()
        conn.close()
        return redirect(url_for('get_users'))

    return render_template('admin/edit.html', user=user)


# Удаление поста
@app.route('/delete_user/<string:username>', methods=('POST',))
def delete_user(username):
    conn = get_db_connection()
    conn.execute('DELETE FROM passwords WHERE login = ?', (username,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_users'))


@app.route("/metrics")
def get_metrics():
    if session.get('role') != 'manager': return redirect(url_for('auth'))
    conn = get_db_connection()
    metrics = conn.execute('''
        SELECT SUM(num_posts), MAX(num_posts), AVG(num_posts)
        FROM passwords
        WHERE role IS NULL;
    ''').fetchone()
    metrics = [{'name': name, 'value': value} for name, value in zip([
        "Кол-во постов",
        "Наибольшее кол-во постов пользователя",
        "Среднее кол-во постов на пользователя"
    ], metrics)]
    conn.close()
    return render_template('admin/metrics.html', metrics=metrics)


@app.route('/account', methods=('GET', 'POST'))
def account():
    return render_template('account/account.html')


# Страница создания нового поста
@app.route('/create_post', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('posts/create.html')


# Страница редактирования поста
@app.route('/edit_post/<int:id>', methods=('GET', 'POST'))
def edit_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_users'))

    return render_template('posts/edit.html', post=post)


# Удаление поста
@app.route('/delete_post/<int:id>', methods=('POST',))
def delete_post(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Post has been deleted.')
    return redirect(url_for('posts'))


@app.route('/logout')
def logout():
    # Удаляем имя пользователя из сессии (выход из аккаунта)
    session.pop('username', None)
    session.clear()  # Очистка всех данных сессии
    return redirect(url_for('index'))


@app.route('/posts')
def posts():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа

    username = session['username']

    # Получаем ID пользователя из таблицы passwords на основе имени пользователя (линк с таблицей posts)
    conn = get_db_connection()

    user_id = conn.execute('SELECT id FROM passwords WHERE login = ?', (username,)).fetchone()
    if user_id is None:
        conn.close()
        return redirect(url_for('login'))  # Если пользователя не существует, перенаправляем на страницу входа

    # Получаем только те посты, которые принадлежат текущему пользователю
    posts = conn.execute('SELECT * FROM posts WHERE user_id = ?', (user_id['id'],)).fetchall()
    conn.close()

    # Рендерим страницу для просмотра "Мои посты"
    return render_template('posts.html', posts=posts, username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
