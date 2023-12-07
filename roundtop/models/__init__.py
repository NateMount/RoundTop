# [Init - Models]

from roundtop import db

# Example of DataBase Model for Roundtop
class UserDemo(db.Model):
    __table_name__:str = 'user_demo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first = db.Column(db.String(25), nullable=False)
    last = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(32))
