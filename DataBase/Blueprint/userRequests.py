from app import app

from DataBase.schemas import (
    UserSchema)

from DataBase.db_utils import (
    create_entry,
    get_entries,
    get_entry_by_id,
    get_entry_by_username,
    update_entry_by_id,
    delete_entry_by_id,
)

from DataBase.models import User

from flask import request, jsonify


@app.route("/user", methods=["POST"])  # create new user
def create_user():
    user_data = UserSchema().load(request.get_json())
    return create_entry(User, UserSchema, **user_data)


@app.route("/user", methods=["GET"])  # get all users
def get_user():
    return get_entries(User, UserSchema)


@app.route("/user/<int:id>", methods=["GET"])  # get user by id
def get_user_by_id(id):
    return get_entry_by_id(User, UserSchema, id)


@app.route("/user/<string:username>", methods=["GET"])  # get user by username
def get_user_by_username(username):
    return get_entry_by_username(User, username)


@app.route("/user/<int:id>", methods=["PUT"])  # update user by id
def update_user_by_id(id):
    user_data = UserSchema().load(request.get_json())
    return update_entry_by_id(User, UserSchema, id, **user_data)


@app.route("/user/<int:id>", methods=["DELETE"])  # delete user by id
def delete_user_by_id(id):
    return delete_entry_by_id(User, UserSchema, id)
