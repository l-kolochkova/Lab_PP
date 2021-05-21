
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_migrate import Manager, Migrate, MigrateCommand
aplication = Flask(__name__)
aplication.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/lab_6'
aplication.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
aplication.config['SECRET_KEY'] = 'thisissecret'
bcrypt = Bcrypt(aplication)
db = SQLAlchemy(aplication)
ma = Marshmallow(aplication)
migrate = Migrate(aplication, db)
manager = Manager(aplication)
manager.add_command('db', MigrateCommand)
