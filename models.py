from app import db
from hashlib import sha256
import secrets

class UserKeys(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False,unique=True)
    pwd = db.Column(db.String(),nullable=False)
    api_key = db.Column(db.String(),unique=True) 
    rate_limit = db.Column(db.Integer, default=10000)

    def __init__(self,name , email, pwd):
        self.name = name 
        self.email = email
        self.pwd = self.generate_hash(pwd)
        self.api_key = self.generate_api_key()

    def generate_api_key(self):
        return secrets.token_urlsafe(50)

    def generate_hash(self, val):
        value = bytes(val,'utf-8')
        h = sha256(value)
        h.update(value)
        return h.hexdigest()
