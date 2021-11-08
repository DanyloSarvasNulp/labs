from models import Session
from flask import jsonify
from functools import wraps
from app import app
import sqlalchemy

session = Session()


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def db_lifecycle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ValueError):
                return jsonify({'message': e.args[0], 'type': 'ValueError'}), 400
            elif isinstance(e, AttributeError):
                return jsonify({'message': e.args[0], 'type': 'AttributeError'}), 400
            elif isinstance(e, KeyError):
                return jsonify({'message': e.args[0], 'type': 'KeyError'}), 400
            elif isinstance(e, TypeError):
                return jsonify({'message': e.args[0], 'type': 'TypeError'}), 400
            elif isinstance(e, sqlalchemy.exc.IntegrityError):
                return jsonify({'message': "duplicate unique value", 'type': 'IntegrityError'}), 400
            # elif isinstance(e, sqlalchemy.exc.IntegrityError):
            #     return jsonify({'message': "duplicate unique value", 'type': 'IntegrityError'}), 400
            else:
                raise e

    return wrapper


def session_lifecycle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rez = func(*args, **kwargs)
            session.commit()
            return rez
        except Exception as e:
            session.rollback()
            raise e

    return wrapper


@db_lifecycle
@session_lifecycle
def create_entry(model_class, model_schema, **kwargs):  # POST entity
    entry = model_class(**kwargs)
    session.add(entry)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
def get_entries(model_class, model_schema):  # GET all entries
    entries = session.query(model_class).all()
    return jsonify(model_schema(many=True).dump(entries))


@db_lifecycle
def get_entry_by_id(model_class, model_schema, id):  # GET entry by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
def get_entry_by_username(model_class, model_schema, username):  # GET _user_ by username
    entry = session.query(model_class).filter_by(username=username).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
@session_lifecycle
def update_entry_by_id(model_class, model_schema, id, **kwargs):  # PUT entity by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    for key, value in kwargs.items():
        setattr(entry, key, value)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
@session_lifecycle
def delete_entry_by_id(model_class, model_schema, id):  # DELETE entity by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    session.delete(entry)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
def get_entry_by_ids(model_class, model_schema, user_id, auditorium_id):  # GET access by user and auditorium ids
    entry = session.query(model_class).filter_by(user_id=user_id, auditorium_id=auditorium_id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
@session_lifecycle
def delete_entry_by_ids(model_class, model_schema, user_id, auditorium_id):  # DELETE access by user and auditorium ids
    entry = session.query(model_class).filter_by(user_id=user_id, auditorium_id=auditorium_id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    session.delete(entry)
    return jsonify(model_schema().dump(entry))
