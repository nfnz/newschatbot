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


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    key_word = db.Column(db.String())
    score = db.Column(db.Integer())

    def __init__(self, user_id, key_word, score):
        self.user_id = user_id
        self.key_word = key_word
        self.score = score

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'key_word': self.key_word,
            'user_id': self.user_id,
            'score': self.score,
        }


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String())
    correct_answers = db.Column(db.Boolean, default=False, nullable=False)
    correct_answer_text = db.Column(db.String, default=True)
    incorrect_answer_text = db.Column(db.String, default=True)

    def __init__(self, answer_text, correct_answers, correct_answer_text, incorrect_answer_text):
        self.answer_text = answer_text
        self.correct_answers = correct_answers
        self.correct_answer_text = correct_answer_text
        self.incorrect_answer_text = incorrect_answer_text

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'correct_answer': self.correct_answers,
            'correct_answer_text': self.correct_answer_text,
            'incorrect_answer_text': self.incorrect_answer_text,
        }


class Questions(db.Model):
    __tablename__ = 'questions'

    news_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String())
    question_type= db.Column(db.Integer())

    def __init__(self, news_id, question_text, question_type):
        self.news_id = news_id
        self.question_text = question_text
        self.question_type = question_type

    def __repr__(self):
        return '<id {}>'.format(self.news_id)

    def serialize(self):
        return {
            'news_id': self.news_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
        }