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


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
