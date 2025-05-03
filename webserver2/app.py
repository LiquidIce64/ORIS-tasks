import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from views import UserView, UserList, UserCreate, UserUpdate, UserDelete
from resources import UserResource, UserListResource

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')


@app.route('/')
def index():
    return render_template('index.html')


# Регистрация представлений
app.add_url_rule('/users', view_func=UserList.as_view('user.list', engine=db))
app.add_url_rule('/users/<string:user_id>/', view_func=UserView.as_view('user.view', engine=db))
app.add_url_rule('/users/create/', view_func=UserCreate.as_view('user.create', engine=db))
app.add_url_rule('/users/<string:user_id>/update/', view_func=UserUpdate.as_view('user.update', engine=db))
app.add_url_rule('/users/<string:user_id>/delete/', view_func=UserDelete.as_view('user.delete', engine=db))

if __name__ == "__main__":
    app.run(debug=True)
