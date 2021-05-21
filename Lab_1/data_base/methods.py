from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from data_base import __init__, app, User, db, user_schema, users_schema, Note, note_schema, notes_schema, Tag, \
    tag_schema, history_schema, History
from data_base import models


# app = Flask(__name__)

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    stats_user = request.json['stats_user']
    count_of_messages = request.json['count_of_messages']
    password = request.json['password']

    new_user = User(name, email, stats_user, count_of_messages, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Get All Products
@app.route('/user', methods=['GET'])
def get_users():
    all_products = User.query.all()
    result = users_schema.dump(all_products)
    return jsonify(result.data)


# Get Single Products
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Update a Product
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    email = request.json['email']
    stats_user = request.json['stats_user']
    count_of_messages = request.json['count_of_messages']
    password = request.json['password']

    user.name = name
    user.email = email
    user.stats_user = stats_user
    user.count_of_messages = count_of_messages
    user.password = password
    db.session.commit()

    return user_schema.jsonify(user)


# Delete Product
@app.route('/user/<id>', methods=['DELETE'])
def delete_usert(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/note', methods=['POST'])
def add_note():
    id_users = request.json['id_users']
    name = request.json['name']
    count_of_users = request.json['count_of_users']
    description = request.json['description']

    new_note = Note(id_users, name, count_of_users, description)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)


# Get All Products
@app.route('/note', methods=['GET'])
def get_note():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result.data)


# Get Single Products
@app.route('/note/<id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    return note_schema.jsonify(note)


# Update a Product
@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)

    id_users = request.json['id_users']
    name = request.json['name']
    count_of_users = request.json['count_of_users']
    description = request.json['description']

    note.id_users = id_users
    note.name = name
    note.count_of_users = count_of_users
    note.description = description

    db.session.commit()

    return note_schema.jsonify(note)


# Delete Product
@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()

    return note_schema.jsonify(note)


@app.route('/tags', methods=['POST'])
def add_tag():
    name = request.json['name']
    id_note = request.json['id_note']
    description = request.json['description']

    new_tag = Tag(name, id_note, description)

    db.session.add(new_tag)
    db.session.commit()

    return tag_schema.jsonify(new_tag)


# Get All Products
@app.route('/tags', methods=['GET'])
def get_tags():
    all_tags = Tag.query.all()
    result = users_schema.dump(all_tags)
    return jsonify(result.data)


# Get Single Products
@app.route('/tags/<id>', methods=['GET'])
def get_tag(id):
    tag = Tag.query.get(id)
    return tag_schema.jsonify(tag)


# Update a Product
@app.route('/tags/<id>', methods=['PUT'])
def update_tag(id):
    tag = Tag.query.get(id)

    name = request.json['name']
    id_note = request.json['id_note']
    description = request.json['description']

    tag.name = name
    tag.id_note = id_note
    tag.description = description
    db.session.commit()

    return user_schema.jsonify(tag)


# Delete Product
@app.route('/tags/<id>', methods=['DELETE'])
def delete_tag(id):
    tag = Tag.query.get(id)
    db.session.delete(tag)
    db.session.commit()

    return user_schema.jsonify(tag)


@app.route('/history', methods=['POST'])
def add_history():
    name = request.json['name']
    id_note = request.json['id_note']
    id_users = request.json['id_users']
    description = request.json['description']
    time_of_edit = request.json['time_of_edit']

    new_history = History(name, id_note, id_users, description, time_of_edit)

    db.session.add(new_history)
    db.session.commit()

    return history_schema.jsonify(new_history)


# Get All Products
@app.route('/history', methods=['GET'])
def get_histories():
    all_histories = History.query.all()
    result = users_schema.dump(all_histories)
    return jsonify(result.data)


# Get Single Products
@app.route('/history/<id>', methods=['GET'])
def get_history(id):
    history = History.query.get(id)
    return user_schema.jsonify(history)


# Update a Product
@app.route('/history/<id>', methods=['PUT'])
def update_history(id):
    history = History.query.get(id)

    name = request.json['name']
    id_note = request.json['id_note']
    id_users = request.json['id_users']
    description = request.json['description']
    time_of_edit = request.json['time_of_edit']

    history.name = name
    history.id_note = id_note
    history.id_users = id_users
    history.description = description
    history.time_of_edit = time_of_edit
    db.session.commit()

    return history_schema.jsonify(history)


# Delete Product
@app.route('/history/<id>', methods=['DELETE'])
def delete_tag(id):
    history = History.query.get(id)
    db.session.delete(history)
    db.session.commit()

    return tag_schema.jsonify(history)
# if __name__ == '__main__':
#     app.run(debug=True)
