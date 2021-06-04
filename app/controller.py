import feedparser
from flask import jsonify, Blueprint

from app.config import FEED_URL
from app.service import get_mock_text, get_mock_image, get_article_from_feed, get_articles_from_feed, \
    update_articles_in_db

api = Blueprint('api', __name__)


@api.route('/articles/')
def get_articles():
    return get_articles_from_feed()


@api.route('/articles/<article>/')
def get_article(article):
    return get_article_from_feed(article)


@api.route('/articles/update', methods=['POST'])
def update_articles():
    try:
        counter = update_articles_in_db()
        return {"message": "Added {} records".format(counter)}
    except:
        return {}


# POST /v1/articles/{article_id}/questions/{questionid?} -> question and answers
# POST /v1/articles/{article_id}/questions/{questionid?} -> question and answers


@api.route('/mocktext')
def mock_text():
    return get_mock_text()


@api.route('/mockimage')
def mock_image():
    return get_mock_image()


@api.route('/mockfeed')
def mock_feed():
    feed = feedparser.parse(FEED_URL)
    return jsonify(title=feed['feed']['title'])
