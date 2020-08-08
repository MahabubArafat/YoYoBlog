from datetime import datetime
from app import db


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # look here we just passed in the function,but not the result of the function's calling or executed result, cause when here something is passed as default , the sqlalchemy will automatically execute it
    user_id = db.Column(db.Integer, db.ForeignKey("user._id"))

    def __repr__(self):
        return f"<Post {self.body}>"

