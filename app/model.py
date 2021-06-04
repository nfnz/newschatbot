from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer())
    published_date = db.Column(db.DateTime())
    title = db.Column(db.String())
    creator = db.Column(db.String())
    image_src = db.Column(db.String())
    link_src = db.Column(db.String())
    text = db.Column(db.String())
    keywords = db.Column(db.String())  # TODO list
    media_name = db.Column(db.String())

    def __init__(self, article_id, published_date, title, creator, image_src, link_src, text, keywords, media_name):
        self.article_id = article_id
        self.published_date = published_date
        self.title = title
        self.creator = creator
        self.image_src = image_src
        self.link_src = link_src
        self.text = text
        self.keywords = keywords
        self.media_name = media_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'published_date': self.published_date,
            'creator': self.creator,
            'image_src': self.image_src,
            'link_src': self.link_src,
            'text': self.text,
            'keywords': self.keywords,
            'media_name': self.media_name,

        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.String())
    keywords = db.Column(db.String())

    def __init__(self, messanger_id, keywords):
        self.messenger_id = messanger_id
        self.keywords = keywords

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'messenger_id': self.messenger_id,
            'keywords': self.keywords,
        }


class Reading(db.Model):
    __tablename__ = 'reading'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(Integer, ForeignKey('articles.id'))
    user_id = db.Column(Integer, ForeignKey('users.id'))
    attention = db.Column(db.Integer())
    like = db.Column(db.Integer())
    refused = db.Column(db.Boolean())
    read = db.Column(db.Boolean())
    score = db.Column(db.Integer())

    def __init__(self, article_id, user_id, attention, like, refused, read, score):
        self.article_id = article_id
        self.user_id = user_id
        self.attention = attention
        self.like = like
        self.refused = refused
        self.read = read
        self.score = score


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'user_id': self.user_id,
            'attention': self.attention,
            'like': self.like,
            'refused': self.refused,
            'read': self.read,
            'score': self.score
        }