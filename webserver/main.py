from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route("/get_example")
def get_example():
    framework = request.args.get('framework')
    language = request.args.get('language')
    version = request.args.get('version')
    return "language = {};framework = {}; version = {} ".format(language, framework, version)


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute((f'''
            SELECT password FROM passwords
            WHERE login = '{login}';
        ''').format())
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != password:
                return render_template('auth_fail.html')
        except:
            return render_template('auth_fail.html')

        db_lp.close()
        return render_template('auth_success.html')

    return render_template('auth.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = f"INSERT INTO passwords VALUES('{login}','{password}');"

        cursor_db.execute(sql_insert)
        db_lp.commit()

        cursor_db.close()
        db_lp.close()

        return render_template('registration_success.html')

    return render_template('registration.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
