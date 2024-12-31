from modules import db,login_manager
from flask_login import UserMixin
from datetime import datetime
import pickle
from sqlalchemy.types import TypeDecorator, PickleType,String

import json

    
@login_manager.user_loader
def load_user(user_id):
    return User_mgmt.query.get(int(user_id))

# class User_mgmt(UserMixin, db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(15),nullable=False,unique=True)
#     email = db.Column(db.String(50),nullable=False,unique=True)
#     password = db.Column(db.String(80),nullable=False)
#     image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
#     bg_file = db.Column(db.String(20),nullable=False,default='default_bg.jpg')
#     bio = db.Column(db.String(200))
#     date = db.Column(db.String(20))
#     bday = db.Column(db.String(10))

#     posts = db.relationship('Post',backref='author',lazy=True)
#     retwitted = db.relationship('Retweet',backref='retwitter',lazy=True)
#     bookmarked = db.relationship('Bookmark',backref='saved_by',lazy=True)


class User_mgmt(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    bg_file = db.Column(db.String(20), nullable=False, default='default_bg.jpg')
    bio = db.Column(db.String(200))
    date = db.Column(db.String(20))
    bday = db.Column(db.String(10))

    # Fields for tracking streak and points
    points = db.Column(db.Integer, default=0)
    last_login = db.Column(db.Date, nullable=True)  # To track the last login date
    streak_days = db.Column(db.Integer, default=0)  # Number of consecutive streak days
    level = db.Column(db.Integer, default=1)  # Track level (1 or 2)
    daily_points = db.Column(db.Integer, default=0)
    selected_theme = db.Column(db.String(100), nullable=True)  # Selected theme for the user



    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    retwitted = db.relationship('Retweet', backref='retwitter', lazy=True)
    bookmarked = db.relationship('Bookmark', backref='saved_by', lazy=True)
    bought_themes = db.Column(String, default=[])  # List of bought themes


    def set_bought_themes(self, themes):
        self.bought_themes = json.dumps(themes)  # Serialize to JSON string
        db.session.commit()

    def get_bought_themes(self):
        return json.loads(self.bought_themes)  # Deserialize from JSON string

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet = db.Column(db.String(500),nullable=False)
    stamp = db.Column(db.String(20),nullable=False)
    post_img = db.Column(db.String(20))
    user_id = db.Column(db.Integer,db.ForeignKey('user_mgmt.id'),nullable=False)

    retweets = db.relationship('Retweet',backref='ori_post',lazy=True)
    timeline = db.relationship('Timeline',backref='from_post',lazy=True)
    bookmark = db.relationship('Bookmark',backref='saved_post',lazy=True)

class Retweet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user_mgmt.id'),nullable=False)
    retweet_stamp = db.Column(db.String(20),nullable=False)
    retweet_text = db.Column(db.String(500),nullable=False)

    timeline = db.relationship('Timeline',backref='from_retweet',lazy=True)

class Timeline(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),default=None)
    retweet_id = db.Column(db.Integer,db.ForeignKey('retweet.id'),default=None)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user_mgmt.id'),default=None)