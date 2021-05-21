from datetime import datetime
#
from data_base import db, ma
#

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
