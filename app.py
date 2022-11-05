from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config 
from flask_migrate import Migrate

app = Flask (__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migate= Migrate(app=app, db=db)

import routes

