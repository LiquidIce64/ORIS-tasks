from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import fields as ma_fields, ValidationError
from models import User, db
from flask import request


ma = Marshmallow()


class UserSchema(ma.Schema):
    id = ma_fields.Integer(dump_only=True)
    username = ma_fields.String(required=True)
    display_name = ma_fields.String(required=True)
    password = ma_fields.String(required=True)
    email = ma_fields.String(required=False)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    def get(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user = db.session.execute(query).scalar()

        if user:
            return users_schema.dump(user)
        return {"status": 404}, 404

    def patch(self, user_id: int):
        query = User.query.where(User.id == user_id)
        if user := db.session.execute(query).scalar():
            if username := request.json.get("username"):
                user.username = username
            if display_name := request.json.get("display_name"):
                user.display_name = display_name
            if password := request.json.get("password"):
                user.password = password
            if email := request.json.get("email"):
                user.email = email
            db.session.commit()
            return {"status": 200}
        return {"status": 404}, 404

    def delete(self, user_id: int):
        query = User.query.where(User.id == user_id)
        if user := db.session.execute(query).scalar():
            db.session.delete(user)
            db.session.commit()
            return {"status": 200}
        return {"status": 404}, 404


class UserListResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)

    def post(self):
        data = request.json
        if not data:
            return {"error": "Request body must be JSON"}, 400

        try:
            new_item_data = user_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        email = new_item_data['email']
        if email == "": email = None

        new_item = User(
            username=new_item_data['username'],
            display_name=new_item_data['display_name'],
            password=new_item_data['password'],
            email=email
        )
        db.session.add(new_item)
        db.session.commit()

        return user_schema.dump(new_item), 201
