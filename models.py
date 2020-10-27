'''
Instantiate and define database model definitions.
'''
# pylint: disable=no-member
# pylint: disable=redefined-builtin
# pylint: disable=too-few-public-methods
from app import db

class ChatHistory(db.Model):
    '''
    Defines ChatHistory table.
    '''
    id = db.Column(db.Integer, primary_key=True)
    plaintext = db.Column(db.String(280))
    user_name = db.Column(db.String(25))
    pfp_url = db.Column(db.String(150))

    def __init__(self, plaintext, user_name, pfp_url):
        self.plaintext = plaintext
        self.user_name = user_name
        self.pfp_url = pfp_url
    def __repr__(self):
        return "<Message: %s User: %s>" % self.plaintext, self.user_name

class AuthUser(db.Model):
    '''
    Defines AuthHistory table.
    '''
    id = db.Column(db.String(25), primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.email)
        