from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer())
    published_date = Column(DateTime())
    title = Column(String())
    creator = Column(String())
    image_src = Column(String())
    link_src = Column(String())
    text = Column(String())
    keywords = Column(String())  # TODO list
    media_name = Column(String())

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

    # TODO Move to service
    def article_article_detail_dto_converter(self, page = 0) -> list:
        # TODO case if article has more than one question
        question = Questions.query.filter(Questions.news_id == self.id).limit(1).one()
        words = self.text.split()
        words_per_page = 25
        words_this_page = words[words_per_page * page:(words_per_page * (page + 1))]
        has_next_page = len(words) > (words_per_page * (page + 1))
        next_page = (page + 1) if has_next_page else page
        data = [{"text": ' '.join(words_this_page)},
                {"attachment": {
                    "payload": {
                        "buttons": [

                            {
                                "url": self.link_src,
                                "title": "přejít na článek",
                                "type": "web_url"
                            }
                        ],
                        "template_type": "button",
                        "text": "Chcete vědět víc?"
                    },
                    "type": "template"
                }},
                {

                            "text": "Článek je",
                            "quick_replies": [
                                {
                                    "type": "show_block",
                                    "block_names": [
                                        "Article" if has_next_page else "Question"
                                    ],
                                    "set_attributes": {"ArticleID": self.id,
                                                       "QuestionID": question.id,
                                                       "Page": next_page},
                                    "title": "super"
                                },
                                {
                                    "type": "show_block",
                                    "block_names": [
                                        "Article" if has_next_page else "Question"
                                    ],
                                    "set_attributes": {"ArticleID": self.id,
                                                       "QuestionID": question.id,
                                                       "Page": next_page},
                                    "title": "ok"
                                },
                                {
                                    "type": "show_block",
                                    "block_names": [
                                        "Articles"
                                    ],
                                    "title": "nuda"
                                }
                            ]


                }
                ]
        if (page == 0): # prepend title and image for the first page
            return [{"text": self.title},
                {"attachment": {"type": "image", "payload": {'url': self.image_src}}}] + data
        else: # return just the text and quick replies on consecutive pages
            return data

    # TODO Move to service
    def article_article_dto_converter(self) -> dict:
        buttons = [{"type": "show_block",
                    "title": "TO MĚ ZAJIMÁ",
                    "block_names": ["Article"],
                    "set_attributes": {"ArticleID": self.id}}]

        return {'title': self.title, 'image_url': self.image_src,
                'buttons': buttons}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    messenger_id = Column(String())
    keywords = Column(String())

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


class Reading(Base):
    __tablename__ = 'reading'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    attention = Column(Integer())
    like = Column(Integer())
    refused = Column(Integer())
    read = Column(Integer())
    score = Column(Integer())

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


class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key_word = Column(String())
    score = Column(Integer())

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

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('articles.id'))
    question_text = Column(String())
    question_type= Column(Integer())
    order = Column(Integer())

    def __init__(self, news_id, question_text, question_type, order):
        self.news_id = news_id
        self.question_text = question_text
        self.question_type = question_type
        self.order = order

    def __repr__(self):
        return '<id {}>'.format(self.news_id)

    def serialize(self):
        return {
            'news_id': self.news_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
        }

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_text = Column(String())
    correct_answers = Column(Boolean)
    correct_answer_text = Column(String)
    order = Column(Integer)
    def __init__(self, question_id, answer_text, correct_answers, correct_answer_text, order):
        self.question_id = question_id
        self.answer_text = answer_text
        self.correct_answers = correct_answers
        self.correct_answer_text = correct_answer_text
        self.order = order

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'correct_answer': self.correct_answers,
            'correct_answer_text': self.answer_text,
            # 'incorrect_answer_text': self.incorrect_answer_text,
        }


