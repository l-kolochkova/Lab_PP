from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt, check_password_hash
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify, render_template, make_response, redirect, flash
from flask_migrate import Manager, Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jwt
from functools import wraps
from flask_login import login_user, login_required, logout_user

# from data_base.methods import add_user
# from data_base.models import User, Note, Tag, History

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/lab_6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    stats_user = db.Column(db.String(70), nullable=False)
    count_of_messages = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(70), nullable=False)

    def __init__(self, name, email, stats_user, count_of_messages, password):
        self.name = name
        self.email = email
        self.stats_user = stats_user
        self.count_of_messages = count_of_messages
        self.password = password


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    id_users = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"))
    name = db.Column(db.String(70), unique=True, nullable=False)
    count_of_users = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(70), nullable=False)

    def __init__(self, id_user, name, count_of_users, description):
        self.id_users = id_user
        self.name = name
        self.count_of_users = count_of_users
        self.description = description


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    id_note = db.Column(db.Integer, db.ForeignKey(Note.id, ondelete="cascade"))
    description = db.Column(db.String(70), nullable=False)

    def __init__(self, name, id_note, description):
        self.name = name
        self.id_note = id_note
        self.description = description


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    id_note = db.Column(db.Integer, db.ForeignKey(Note.id, ondelete="cascade"))
    id_users = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"))
    description = db.Column(db.String(70), nullable=False)
    time_of_edit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, name, id_note, id_users, description, time_of_edit):
        self.name = name
        self.id_note = id_note
        self.id_users = id_users
        self.description = description
        self.time_of_edit = time_of_edit


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'stats_user', 'count_of_messages', 'password')


class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_users', 'name', 'count_of_users', 'description')


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_note', 'email', 'description')


class HistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'id_note', 'id_users', 'description', 'time_of_edit')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
history_schema = HistorySchema()
histories_schema = HistorySchema(many=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            #print(jsonify({'message': token}))
            return jsonify({'message':  'Token is missing!!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': token + ' Token is invalid!!!'}), 401
        return f(*args, **kwargs)

    return decorated


@app.route('/logout')
def unprotected():
    # logout_user()
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected():
    # if not current_user.admin:
    #   return jsonify({'message': 'Cannot perform that function!'})
    return jsonify({'message': 'This is only available for people with valid tokens.'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.password or not auth.username:
        return make_response('Could verify!', 401, {'WWW-authenticate': 'Basic realm="Login Required'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return jsonify({'message': 'No user found!'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could verify!', 401, {'WWW-authenticate': 'Basic realm="Login Required'})
    # login = request.form.get('login')
    # password = request.form.get('password')
    #
    # if login and password:
    #     user = User.query.filter_by(login=login).first()
    #
    #     if user and check_password_hash(user.password, password):
    #         login_user(user)
    #
    #         next_page = request.args.get('next')
    #
    #         return redirect(next_page)
    #     else:
    #         flash('Login or password is not correct')
    # else:
    #     flash('Please fill login and password fields')
    #
    # return "login complete"


@app.route("/api/v1/hello-world-/<num_of_variant>")
def hello_world(num_of_variant):
    # user = User("Yaroslav", "exp@smth.com", 22, 22)
    user = User("Oleg", "exampe@dd.com", "stats", 3, 312312)
    note = Note(14, "Forest", 4, "For adult")
    d1 = datetime(2017, 3, 5, 12, 30, 10)

    tag = Tag("chilling", 14, "on the beach")
    history = History("new_changes", 14, 13, "new user_3", d1)
    db.session.add(user)
    # db.session.add(note)
    # db.session.add(tag)
    # db.session.add(history)
    db.session.commit()
    return 'Hello, World! {' + num_of_variant + '}'


@app.route('/users', methods=['POST'])
@token_required
def add_user():
    name = request.json['name']
    email = request.json['email']
    stats_user = request.json['stats_user']
    count_of_messages = request.json['count_of_messages']
    password = request.json['password']
    if name is "" or email is "" or password is "" or stats_user is "" or count_of_messages is "":
        return "Invalid body", 400
    password_hash = bcrypt.generate_password_hash(password)
    new_user = User(name, email, stats_user, count_of_messages, password_hash)
    all_users = User.query.all()
    for user in all_users:
        if user.email == email:
            return "User with such email already exists", 409
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.errorhandler(404)
def not_found(e):
    return jsonify(message="You do not have access!", status=404)


@app.errorhandler(405)
def not_found(e):
    return jsonify(message="You do not have access!", status=405)


@app.errorhandler(500)
def not_found(e):
    return jsonify(message="You do not have access!", status=500)


@app.errorhandler(403)
def not_found(e):
    return jsonify(message="You do not have access!", status=403)


# Get All Products
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Get Single Products
@app.route('/users/<id>', methods=['GET'])
@token_required
def get_user(id):
    #if not current_user.id == 31:
     #   return jsonify({'message': 'Cannot perform that function!'})
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Update a Product
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    email = request.json['email']
    stats_user = request.json['stats_user']
    count_of_messages = request.json['count_of_messages']
    password = request.json['password']
    password_hash = bcrypt.generate_password_hash(password)
    if name is "" or email is "" or password is "" or stats_user is "" or count_of_messages is "":
        return "Invalid body", 400
    user.name = name
    user.email = email
    user.stats_user = stats_user
    user.count_of_messages = count_of_messages
    user.password = password_hash
    db.session.commit()

    return user_schema.jsonify(user)


# Delete Product
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/note', methods=['POST'])
@token_required
def add_note():
    id_users = request.json['id_users']
    name = request.json['name']
    count_of_users = request.json['count_of_users']
    description = request.json['description']
    all_notes = Note.query.all()
    if name is "" or id_users is "" or count_of_users is "" or description is "":
        return "Invalid body", 400
    for note in all_notes:
        if note.name == name:
            return "Note with such name already exists", 409
    new_note = Note(id_users, name, count_of_users, description)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)


# Get All Products
@app.route('/note', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)


# Get Single Products
@app.route('/note/<id>', methods=['GET'])
@token_required
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
    if name is "" or id_users is "" or count_of_users is "" or description is "":
        return "Invalid body", 400
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
@token_required
def add_tag():
    name = request.json['name']
    id_note = request.json['id_note']
    description = request.json['description']
    all_tags = Tag.query.all()
    if name is "" or id_note is "" or description is "":
        return "Invalid body", 400
    for tag in all_tags:
        if tag.name == name:
            return "Note with such name already exists", 409
    new_tag = Tag(name, id_note, description)
    db.session.add(new_tag)
    db.session.commit()

    return tag_schema.jsonify(new_tag)


# Get All Products
@app.route('/tags', methods=['GET'])
def get_tags():
    all_tags = Tag.query.all()
    result = users_schema.dump(all_tags)
    return jsonify(result)


# Get Single Products
@app.route('/tags/<id>', methods=['GET'])
@token_required
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
    if name is "" or id_note is "" or description is "":
        return "Invalid body", 400
    tag.name = name
    tag.id_note = id_note
    tag.description = description
    db.session.commit()

    return tag_schema.jsonify(tag)


# Delete Product
@app.route('/tags/<id>', methods=['DELETE'])
def delete_tag(id):
    tag = Tag.query.get(id)
    db.session.delete(tag)
    db.session.commit()

    return tag_schema.jsonify(tag)


@app.route('/history', methods=['POST'])
@token_required
def add_history():
    name = request.json['name']
    id_note = request.json['id_note']
    id_users = request.json['id_users']
    description = request.json['description']
    time_of_edit = request.json['time_of_edit']
    all_histories = History.query.all()
    if name is "" or id_note is "" or id_users is "" or description is "" or time_of_edit is "":
        return "Invalid body", 400
    for history in all_histories:
        if history.name == name:
            return "Note with such name already exists", 409
    new_history = History(name, id_note, id_users, description, time_of_edit)

    db.session.add(new_history)
    db.session.commit()

    return history_schema.jsonify(new_history)


# Get All Products
@app.route('/history', methods=['GET'])
def get_histories():
    all_histories = History.query.all()
    result = histories_schema.dump(all_histories)
    return jsonify(result)


# Get Single Products
@app.route('/history/<id>', methods=['GET'])
@token_required
def get_history(id):
    history = History.query.get(id)
    return history_schema.jsonify(history)


# Update a Product
# @app.route('/history/<id>', methods=['PUT'])
# def update_history(id):
#     history = History.query.get(id)
#
#     name = request.json['name']
#     id_note = request.json['id_note']
#     id_users = request.json['id_users']
#     description = request.json['description']
#     time_of_edit = request.json['time_of_edit']
#
#     history.name = name
#     history.id_note = id_note
#     history.id_users = id_users
#     history.description = description
#     history.time_of_edit = time_of_edit
#     db.session.commit()
#
#     return history_schema.jsonify(history)
#
#
# # Delete Product
# @app.route('/history/<id>', methods=['DELETE'])
# def delete_history(id):
#     history = History.query.get(id)
#     db.session.delete(history)
#     db.session.commit()
#
#     return history_schema.jsonify(history)


app.debug = True
# manager.run()
http_server = WSGIServer(('127.0.0.1', 8082), app)
http_server.serve_forever()
