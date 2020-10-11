# models.py
import flask_sqlalchemy
from app import db

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plaintext = db.Column(db.String(280))
    userName = db.Column(db.String(25))
    
    def __init__(self, plaintext, userName):
        self.plaintext = plaintext
        self.userName = userName
        
    def __repr__(self):
        return '<Message: %s User: %s>' % self.plaintext, self.userName