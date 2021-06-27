import feedparser
from flask import jsonify
from datetime import datetime
import requests
from newschatbot.app.config import FEED_URL, FEED_FOR_QUESTIONS
from newschatbot.app.model import Article, db, Questions, Answers
import xmltodict

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

            new_question = Questions(news_id=i, question_text=q['QUIZ']['QUIZ_TITLE'],
                                             question_type='basic', order=order)

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


def verify_answer(answerID):
    answer = Answers.query.get(answerID)
    question = Questions.query.filter(Questions.id == answer.question_id).limit(1).one()
    article = Article.query.filter(Article.id == question.news_id).limit(1).one()

    result = "Trefa! Pokud se chcete dozvědět víc, koukněte na článek:" if answer.correct_answers \
        else 'To se nepovedlo. Koukněte na článek:'

    return jsonify({
        "messages": [
            {"attachment": {
                "payload": {
                    "buttons": [

                        {
                            "url": article.link_src,
                            "title": "Chcete vědět víc?",
                            "type": "web_url"
                        }
                    ],
                    "template_type": "button",
                    "text": result
                },
                "type": "template"
            }}]
    })

def update_questions():
    response = requests.get(FEED_FOR_QUESTIONS)
    db_questions = Questions.query.all()
    articles_id_in_questions = [question.article_id for question in db_questions]
    db_articles = Article.query.all()
    data = xmltodict.parse(response.content)
    for key, value in data.items():
        order = 0
        for i, j in value.items():
            for q in j:
                if int(q['ID']) not in articles_id_in_questions:
                    id_for_article_id = [article.id if article.article_id == q['ID'] else None for article in db_articles]
                    order += 1
                    new_question = Questions(news_id=id_for_article_id[0], question_text=q['QUIZ']['QUIZ_TITLE'],
                                             question_type='basic', order=order)
                    db.session.add(new_question)
    db.session.commit()


