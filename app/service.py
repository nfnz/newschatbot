import feedparser

from flask import jsonify, request
from sqlalchemy import and_, or_, Date, cast, func
from datetime import datetime, date, timedelta
from flask_paginate import Pagination, get_page_args
from typing import List

from app.config import FEED_URL
from app.model import Article, Reading, User, db, Questions, Answers, Score

ROWS_PER_PAGE = 5

BONUS_START = 3


def get_mock_text():
    return {
        "messages": [
            {"text": "Welcome to the Chatfuel Rockets!"},
            {"text": "What are you up to?"},
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
                    },
                }
            }
        ]
    }


def get_articles_from_feed():
    feed = feedparser.parse(FEED_URL)
    l = []
    for i in feed["entries"]:
        d = {
            "title": i["title"],
            "image_url": i["szn_image"],
            "buttons": [
                {
                    "type": "show_block",
                    "title": "TO MĚ ZAJIMÁ",
                    "block_names": ["Article"],
                    "set_attributes": {"ArticleID": i["id"], "Page": 0},
                }
            ],
        }
        l.append(d)
    response = jsonify(
        {
            "messages": [
                {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "image_aspect_ratio": "square",
                            "elements": l[:5],
                        },
                    }
                }
            ]
        }
    )
    return response


def get_article_from_feed(article):
    feed = feedparser.parse(FEED_URL)
    d = {}
    for i in feed["entries"]:
        if i["id"] == str(article):
            d["title"] = i["title"]
            d["image"] = {"type": "image", "payload": {"url": i["szn_image"]}}
            d["summary"] = i["summary"]
    response = jsonify(
        {
            "messages": [
                {"text": d["title"]},
                {"attachment": d["image"]},
                {"text": d["summary"]},
            ]
        }
    )
    return response


def update_articles_in_db():
    feed = feedparser.parse(FEED_URL)
    counter = 0

    db_articles = Article.query.all()
    db_articles_ids = [article.article_id for article in db_articles]

    for i in feed["entries"]:
        if int(i["id"]) not in db_articles_ids:
            published_date = datetime.strptime(
                i["published"], "%a, %d %b %Y %H:%M:%S %z"
            )

            new_article = Article(
                article_id=i["id"],
                published_date=published_date,
                title=i["title"],
                creator=i["author"],
                image_src=i["szn_image"],
                link_src=i["link"],
                text=i["summary"],
                keywords="TODO",
                media_name="cti-doma",
            )

            db.session.add(new_article)
            counter = counter + 1
    db.session.commit()
    return counter


def articles_to_chatfuel_list(articles, current_page, total_articles):
    results = [article.article_article_dto_converter() for article in articles.items]
    if (
            current_page * ROWS_PER_PAGE < total_articles
    ):  # do not append when there are no more articles
        results.append(
            {
                "title": "Více",
                "buttons": [
                    {
                        "type": "show_block",
                        "block_names": ["Articles"],
                        "set_attributes": {"Page": current_page + 1},
                        "title": "Starší zprávy",
                    },
                ],
            }
        )

    return jsonify(
        {
            "messages": [
                {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "image_aspect_ratio": "square",
                            "elements": results,
                        },
                    }
                }
            ]
        }
    )


def get_articles_from_db():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.published_date.desc()).paginate(
        page=page, per_page=ROWS_PER_PAGE
    )
    total_articles = Article.query.count()
    return articles_to_chatfuel_list(articles, page, total_articles)


def get_unread_articles_from_db(user_data):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(
        messenger_id=str(user_data["messenger user id"])
    ).first()
    if not user:
        return get_articles_from_db()
    articles = (
        Article.query.outerjoin(
            Reading,
            and_(Article.id == Reading.article_id, Reading.user_id == user.id),
            aliased=True,
        )
            .filter(or_(Reading.refused == 0, Reading.refused == None))
            .filter(or_(Reading.read == 0, Reading.read == None))
            .order_by(Article.published_date.desc())
            .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    )
    total_articles = (
        Article.query.outerjoin(
            Reading,
            and_(Article.id == Reading.article_id, Reading.user_id == user.id),
            aliased=True,
        )
            .filter(or_(Reading.refused == 0, Reading.refused == None))
            .filter(or_(Reading.read == 0, Reading.read == None))
            .count()
    )
    return articles_to_chatfuel_list(articles, page, total_articles)


def get_article_from_db(pk_id, page=0):
    article = Article.query.get(pk_id)
    return jsonify({"messages": article.article_article_detail_dto_converter(page)})


def get_question_from_db(questionID):
    question = Questions.query.get(questionID)
    answears = Answers.query.filter(Answers.question_id == question.id).all()
    article: Article = Article.query.filter(Article.id == question.news_id).one()

    buttons = []
    for i in answears:
        d = {
            "block_names": ["ShowTextTest"],
            "set_attributes": {
                "ArticleID": question.news_id,
                "QuizID": question.id,
                "AnswerID": i.id,
            },
            "title": i.answer_text,
            "type": "show_block",
        }
        buttons.append(d)

    return jsonify(
        {"messages": [{"quick_replies": buttons, "text": question.question_text}]}
    )


def get_total_score(user_id: int) -> int:
    return (
        db.session.query(func.sum(Score.score))
            .filter(Score.user_id == user_id)
            .scalar()
    )


def get_score_correct_shape(score: int) -> str:
    if score == 0:
        return "bodů"
    if score == 1:
        return "bod"
    if score < 5:
        return "body"
    return "bodů"


def get_answer_text(correct_answer: bool, yesterday_score: int, user_id: int) -> str:
    def get_reminder() -> str:
        date_today = date.today()
        today_score: Score = get_score(user_id, date_today)
        if today_score.score == 2:
            return "Ještě jednu otázku a zítra se ti body násobí 2x\n"
        elif today_score.score == 0:
            return "Když dáš dnes 3 správné odpovědi, zítra se ti body násobí 2x"
        elif today_score.score < 2:
            return (
                f"Dnes jsi správně odpověděl {today_score.score} {'otázek' if today_score == 0 else 'otázku'}, "
                f"když dáš 3, zítra se ti body násobí 2x"
            )
        return ""

    text = ""
    if correct_answer:
        text += "Trefa! Jde ti to. 👍\n"
        user_score: List[Score] = Score.query.filter(Score.user_id == user_id).all()
        # it would be better to do the sum directly in database,
        # I just don't know how now
        total_score = sum(score.score for score in user_score)
        if yesterday_score < BONUS_START:
            text += f"Dám ti 1 bod, celkem máš {total_score} {get_score_correct_shape(total_score)}.\n"
        else:
            text += f"Dám ti 2 body, celkem máš {total_score} {get_score_correct_shape(total_score)}.\n"
        text += get_reminder()
        return text

    text += "To se nepovedlo, ale nevadí 👍"
    text += get_reminder()
    return text


def verify_answer(answerID, user_data):
    user = _ensure_user(user_data)
    yesterday_score = get_score(user.id, date.today() - timedelta(days=1))

    answer = Answers.query.get(answerID)
    question = Questions.query.filter(Questions.id == answer.question_id).limit(1).one()
    article = Article.query.filter(Article.id == question.news_id).limit(1).one()
    article_questions = (
        Questions.query.filter(Questions.news_id == question.news_id)
            .order_by(Questions.order, Questions.id)
            .all()
    )
    question_index = article_questions.index(question)
    has_more_questions = len(article_questions) > (question_index + 1)

    if answer.correct_answers:
        increase_score(
            article.id, user_data, 1 if yesterday_score.score < BONUS_START else 2
        )

    result = get_answer_text(
        correct_answer=answer.correct_answers,
        yesterday_score=yesterday_score.score,
        user_id=user.id,
    )

    buttons = [
        {"url": article.link_src, "title": "Chcete vědět víc?", "type": "web_url"},
        {
            "type": "show_block",
            "title": "Další zprávy",
            "block_names": ["Articles"],
            "set_attributes": {"ArticleID": article.id},
        },
    ]
    if has_more_questions:
        next_question = article_questions[
            question_index + 1
            ]  # safe, because has_more_questions checks the list length
        buttons.append(
            {
                "type": "show_block",
                "title": "Další otázka",
                "block_names": ["Question"],
                "set_attributes": {
                    "ArticleID": article.id,
                    "QuestionId": next_question.id,
                },
            }
        )

    return jsonify(
        {
            "messages": [
                {
                    "attachment": {
                        "payload": {
                            "buttons": buttons,
                            "template_type": "button",
                            "text": result,
                        },
                        "type": "template",
                    }
                }
            ]
        }
    )


def _ensure_user(user_data):
    user = User.query.filter_by(
        messenger_id=str(user_data["messenger user id"])
    ).first()
    if not user:
        user = User(
            messenger_id=str(user_data["messenger user id"]),
            keywords=user_data.get("keywords"),
        )
        db.session.add(user)
        db.session.commit()
    return user


def _ensure_reading(user_id, article_id):
    reading = Reading.query.filter_by(user_id=user_id, article_id=article_id).first()
    if not reading:
        reading = Reading(
            article_id=article_id,
            user_id=user_id,
            attention=0,
            like=0,
            refused=0,
            read=0,
            score=0,
        )
        db.session.add(reading)
        db.session.commit()
    return reading


def set_article_not_interested(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.refused = 1
    db.session.commit()


def set_article_read(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.read = 1
    db.session.commit()


def get_score(user_id: int, date: date) -> Score:
    score = Score.query.filter(
        and_(cast(Score.date, Date) == date, Score.user_id == user_id)
    ).one_or_none()
    if score is not None:
        return score

    return Score(
        user_id=user_id,
        key_word="",
        score=0,
        date=date,
    )


def increase_score(article_id, user_data, amount: int):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.score = reading.score + amount
    score = get_score(user.id, date.today())
    score.score += amount
    db.session.add(score)
    db.session.commit()


def set_article_liked(article_id, user_data):
    user = _ensure_user(user_data)
    reading = _ensure_reading(user.id, article_id)
    reading.like = reading.like + 1
    db.session.commit()


def text_new_user(user_data):
    first_name = user_data["first name"]
    return (
        f"Hellou, {first_name}.\n"
        f"Jsem moc rád, že jsi tu. Mým úkolem je totiž ukázat co nejvíce lidem, že mít přehled o dění ve světě a čtení novinek je zábava!\n\n"
        f"Takže si spolu zahrajeme hru, jo? 😜"
    )


def text_returned_user(user_data, user: User, total_score):
    first_name = user_data["first name"]
    date_today = date.today()
    date_week_ago = date_today - timedelta(days=7)
    week_score = (
                     db.session.query(func.sum(Score.score))
                         .filter(Score.date.between(date_week_ago, date_today))
                         .scalar()
                 ) or 0
    yesterday_score = get_score(user.id, date.today() - timedelta(days=1)).score
    final_text = ""
    if yesterday_score >= 3:
        final_text = (
            f"Včera jsi získal {yesterday_score} {get_score_correct_shape(yesterday_score)}. "
            f"Tvoje body se ti dnes násobí dvěma. "
            f"Mám pro tebe další zprávy."
        )
    return (
        f"Á, {first_name}, vítej zpátky.\n"
        f"Aktuálně máš celkem {total_score} {get_score_correct_shape(total_score)}. "
        f"Za poslední týden jsi získal {week_score} {get_score_correct_shape(week_score)}.\n"
        f"{final_text}"
    )


def get_introduction_text(user_data):
    user = _ensure_user(user_data)
    total_score = get_total_score(user.id) or 0
    if total_score == 0:
        text = text_new_user(user_data)
    else:
        text = text_returned_user(user_data, user, total_score)
    return jsonify(
        {
            "messages": [
                {
                    "text": text,
                    "quick_replies": [
                        {
                            "type": "show_block",
                            "block_names": ["Articles"],
                            "title": "Jdeme na to",
                        },
                        {
                            "type": "show_block",
                            "block_names": ["Articles"],
                            "title": "Odběr",
                        },
                    ],
                }
            ],
        }
    )
