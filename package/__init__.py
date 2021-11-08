from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
# from package.models import metadata as YOUR_FILENAME_metadata
from sqlalchemy import text
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjhfghjsdgfjhgjdshgfjh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_20:123@159.69.151.133:5056/user_20_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# metadata = [YOUR_FILENAME_metadata]
db = SQLAlchemy(app)
# db.Model.metadata.reflect(db.engine)
manager = LoginManager(app)


menu = [{"title": "Main Page", "url": "/"},
        {"title": "Login", "url": "/login"},
        {"title": "DB", "url": "/db"},
        {"title": "Logout", "url": "/logout"},
        {"title": "Profile", "url": "/profile"}
        ]


class Size(db.Model):
    __tablename__ = 'sizes'

    size_id = db.Column('size_id', db.Integer, primary_key=True)
    size_name = db.Column('size_name', db.Integer)


class UsersGroup(db.Model):
    __tablename__ = 'users_groups'

    group_id = db.Column('group_id', db.Integer, primary_key=True, server_default=text("nextval('users_groups_group_id_seq'::regclass)"))
    group_name = db.Column('group_name', db.String, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column('user_id', db.BigInteger, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    first_name = db.Column('first_name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    email = db.Column('email', db.String(100), nullable=False)
    phone = db.Column('phone', db.String(30), nullable=False)
    password_1 = db.Column('pass', db.String(32))
    active = db.Column('active', db.Boolean, nullable=False, server_default=text("true"))
    password = db.Column('password', db.String, nullable=False)
    salt = db.Column('salt', db.String, nullable=False)
    created = db.Column('created', db.DateTime)
    group_id = db.Column('group_id', db.ForeignKey('users_groups.group_id'), nullable=False)

    group = relationship('UsersGroup')

    def get_id(self):
        return self.user_id


from package.decorators import *
from package.routes import *
from package.defs import *


# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Vehicle = Base.classes.vehicle
# Users = Base.classes.users
