import feedparser
from flask import jsonify
from datetime import datetime

from app.config import FEED_URL
from app.model import Article, db


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
        d = {}
        d['title'] = i['title']
        d['image_url'] = i['szn_image']
        d['buttons'] = [{"type": "json_plugin_url",
                         "url": "https://qpvtvquvp1.execute-api.eu-central-1.amazonaws.com/dev/articles/{}/".format(
                             i['id']),
                         "title": "TO MĚ ZAJIMÁ"}]
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
