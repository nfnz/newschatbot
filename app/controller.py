import feedparser
from flask import jsonify, Blueprint, request

from app.config import FEED_URL
from app.service import (
    get_mock_text,
    get_mock_image,
    get_article_from_feed,
    get_articles_from_feed,
    set_article_not_interested,
    update_articles_in_db,
    get_articles_from_db,
    get_article_from_db,
    get_question_from_db,
    get_unread_articles_from_db,
    verify_answer,
    set_article_read,
    set_article_liked,
    get_introduction_text,
    get_outro_text,
)

api = Blueprint("api", __name__)


@api.route("/v1/introduction", methods=["POST"])
def get_introduction():
    return get_introduction_text(request.json)


@api.route("/v1/outro", methods=["POST"])
def get_outro():
    return get_outro_text(request.json)


@api.route(
    "/v1/articles/", methods=["GET", "POST"]
)  # TODO: remove GET after updating the Chatfuel block
def get_articles_v1():
    if request.method == "POST":
        return get_unread_articles_from_db(request.json)
    return get_articles_from_db()


@api.route(
    "/v1/articles/<article>/", methods=["GET", "POST"]
)  # TODO: remove GET after updating the Chatfuel block
def get_article_v1(article):
    page = int(request.args.get("page") or 0)
    if request.method == "POST":
        set_article_read(article, request.json)
        set_article_liked(article, request.json)
    return get_article_from_db(article, page)


@api.route("/articles/")
def get_articles():
    return get_articles_from_feed()


@api.route("/articles/<article>/")
def get_article(article):
    return get_article_from_feed(article)


@api.route("/v1/articles/<article>/not-interested", methods=["POST"])
def article_not_interested(article):
    set_article_not_interested(user_data=request.json, article_id=article)
    return get_unread_articles_from_db(request.json)


@api.route("/articles/update", methods=["POST"])
def update_articles():
    try:
        counter = update_articles_in_db()
        return {"message": "Added {} records".format(counter)}
    except:
        return {}


@api.route("/articles/<article>/questions/<question>/")
def get_question(article, question):
    return get_question_from_db(question)


@api.route(
    "/articles/<article>/questions/<questions>/answers/<answer>/",
    methods=["GET", "POST"],
)  # TODO: remove GET after updating the Chatfuel block
def check_answer(article, questions, answer):
    return verify_answer(answer, request.json)


@api.route("/v1/articles/<article>/read", methods=["POST"])
def article_read(article):
    set_article_read(article_id=article, user_data=request.json)
    return get_unread_articles_from_db(request.json)


@api.route("/mocktext")
def mock_text():
    return jsonify(get_mock_text())


@api.route("/mockimage")
def mock_image():
    return jsonify(get_mock_image())


@api.route("/mockfeed")
def mock_feed():
    feed = feedparser.parse(FEED_URL)
    return jsonify(title=feed["feed"]["title"])


@api.after_request
def log_response_info(response):
    print("Log response:")
    print(response.status)
    print(response.get_json())
    return response


@api.before_request
def log_request_info():
    print("Log request:")
    print(request.full_path)
    print(request.get_json())
