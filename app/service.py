import feedparser
from flask import jsonify
from datetime import datetime

from app.config import FEED_URL
from app.model import Article, Reading, User, db, Questions, Answers


def get_mock_text():
    return {
        "messages": [
            {
                "text": "Welcome to the Chatfuel Rockets!"
            },
            {
                "text": "What are you up to?"
            }
        ]
    }


def get_mock_image():
    return {
        "messages": [
            {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": "https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png"
                    }
                }
            }
        ]
    }


def get_articles_from_feed():
    feed = feedparser.parse(FEED_URL)
    l = []
    for i in feed['entries']:
        d = {'title': i['title'], 'image_url': i['szn_image'],
             'buttons': [{"type": "show_block",
                          "title": "TO MĚ ZAJIMÁ",
                          "block_names": ["Article"],
                          "set_attributes": {"ArticleID": i['id']}}]}
        l.append(d)
    response = jsonify({
        "messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "image_aspect_ratio": "square",
                        "elements": l[:5]
                    }
                }
            }
        ]
    })
    return response


def get_article_from_feed(article):
    feed = feedparser.parse(FEED_URL)
    d = {}
    for i in feed['entries']:
        if i['id'] == str(article):
            d['title'] = i['title']
            d['image'] = {"type": "image", "payload": {'url': i['szn_image']}}
            d['summary'] = i['summary']
    response = jsonify({
        "messages": [
            {
                "text": d['title']
            },
            {
                "attachment": d['image']
            },
            {
                "text": d['summary']
            }

        ]
    })
    return response


def update_articles_in_db():
    feed = feedparser.parse(FEED_URL)
    counter = 0

    db_articles = Article.query.all()
    db_articles_ids = [article.article_id for article in db_articles]

    for i in feed['entries']:
        if int(i['id']) not in db_articles_ids:
            published_date = datetime.strptime(i['published'], "%a, %d %b %Y %H:%M:%S %z")

            new_article = Article(article_id=i['id'], published_date=published_date, title=i['title'],
                                  creator=i['author'], image_src=i['szn_image'], link_src=i['link'], text=i['summary'],
                                  keywords='TODO', media_name='cti-doma')

            db.session.add(new_article)
            counter = counter + 1
    db.session.commit()
    return counter


def get_articles_from_db():
    articles = Article.query \
        .order_by(Article.published_date.desc()) \
        .limit(5) \
        .all()

    results = [article.article_article_dto_converter() for article in articles]

    return jsonify({
        "messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "image_aspect_ratio": "square",
                        "elements": results
                    }
                }
            }
        ]
    })


def get_article_from_db(pk_id, page=0):
    article = Article.query.get(pk_id)
    set_article_read(article.id)
    return jsonify({"messages": article.article_article_detail_dto_converter(page)})


def get_question_from_db(questionID):
    question = Questions.query.get(questionID)
    answears = Answers.query.filter(Answers.question_id == question.id).all()

    buttons = []
    for i in answears:
        d = {
            "block_names": [
                "ShowTextTest"
            ],
            "set_attributes": {
                "ArticleID": question.news_id,
                "QuizID": question.id,
                "AnswerID": i.id
            },
            "title": i.answer_text,
            "type": "show_block"
        }
        buttons.append(d)

    return jsonify({
        "messages": [
            {
                "quick_replies": buttons,
                "text": question.question_text
            }
        ]
    })


def verify_answer(answerID, user_data):
    answer = Answers.query.get(answerID)
    question = Questions.query.filter(Questions.id == answer.question_id).limit(1).one()
    article = Article.query.filter(Article.id == question.news_id).limit(1).one()
    article_questions = Questions.query.filter(Questions.news_id == question.news_id).order_by(Questions.order, Questions.id).all()
    question_index = article_questions.index(question)
    has_more_questions = len(article_questions) > (question_index + 1)

    if answer.correct_answers:
        increase_score(article.id, user_data)

    result = "Trefa! Pokud se chcete dozvědět víc, koukněte na článek:" if answer.correct_answers \
        else 'To se nepovedlo. Koukněte na článek:'

    buttons = [
        {
            "url": article.link_src,
            "title": "Chcete vědět víc?",
            "type": "web_url"
        }
    ]
    if has_more_questions:
        next_question = article_questions[question_index + 1] # safe, because has_more_questions checks the list length
        buttons.append({
            "type": "show_block",
            "title": "Další otázka",
            "block_names": [
                "Question"
            ],
            "set_attributes": {
                "ArticleID": article.id,
                "QuestionId": next_question.id
            },
        })

    return jsonify({
        "messages": [
            {"attachment": {
                "payload": {
                    "buttons": buttons,
                    "template_type": "button",
                    "text": result
                },
                "type": "template"
            }}]
    })

def _ensure_user(user_data):
    user = User.query.filter_by(messenger_id=user_data.messenger_user_id).first()
    if not user:
        user = User(user_data.messenger_user_id)
        db.session.add(user)
        db.session.commit()
    return user

def _ensure_reading(user_id, article_id):
    reading = Reading.query.filter_by(user_id=user_id, article_id=article_id)
    if not reading:
        reading = Reading(article_id=article_id, user_id=user_id, attention=0, like=0, refused=False, read=False, score=0)
        db.sesstion.add(reading)
        db.session.commit()
    return reading

def set_article_not_interested(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.refused = True
    db.session.commit()

def set_article_read(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.read = True
    db.session.commit()

def increase_score(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.score = reading.score + 1
    db.session.commit()
