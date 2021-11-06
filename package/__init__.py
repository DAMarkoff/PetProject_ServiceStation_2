from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from models.db_classes import metadata as YOUR_FILENAME_metadata
from package import defs, decorators, routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjhfghjsdgfjhgjdshgfjh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_20:123@159.69.151.133:5056/user_20_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = [YOUR_FILENAME_metadata]
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Vehicle = Base.classes.vehicle
Users = Base.classes.users
