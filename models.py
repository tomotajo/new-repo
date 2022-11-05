from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())
    
    image = db.Column(db.String())

    
    def __repr__(self) -> str:
        return "<Store User: {}>".format(self.username)