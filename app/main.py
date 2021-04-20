import feedparser
from flask import Flask, jsonify
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

from app.config import FEED_URL, POSTGRES_DB_CONN
# from app.models import db, User

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_DB_CONN
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# migrate = Migrate(app, db)


@app.route('/mocktext')
def mock_text():
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


@app.route('/mockimage')
def mock_image():
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


@app.route('/mockfeed')
def mock_feed():
    feed = feedparser.parse(FEED_URL)

    return jsonify(title=feed['feed']['title'])


# GET /v1/articles/tags=?.. -> gallery
@app.route('/articles/')
def get_articles():
    feed = feedparser.parse(FEED_URL)

    l = []
    for i in feed['entries']:
        d = {}
        d['title'] = i['title']
        d['image_url'] = i['szn_image']
        # d['subtitle'] = "Size: M"
        d['buttons'] = [{"type": "web_url", "url": "https://rockets.chatfuel.com/articles/{}/".format(i['id']),
                         "title": "TO MĚ ZAJIMÁ"}]
        l.append(d)

    return jsonify({
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


# GET /v1/articles/{article_id}/ -> header, photo, short text
@app.route('/articles/<article>/')
def get_article(article):
    feed = feedparser.parse(FEED_URL)

    d = {}
    for i in feed['entries']:
        if i['id'] == str(article):
            d['title'] = i['title']
            d['image'] = {"type": "image", "payload": {'url': i['szn_image']}}
            d['summary'] = i['summary']

    return jsonify({
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


# GET /v1/articles/{article_id}/questions/{questionid?} -> question and answers
# POST /v1/articles/{article_id}/questions/{questionid?} -> question and answers


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
