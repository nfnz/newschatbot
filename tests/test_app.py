import psycopg2
from flask import Flask
import feedparser
from datetime import date, timedelta


# TODO: is test_get_articles_v1_post necessary?
def test_get_articles_v1_get(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/v1/articles/?page=1")
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {
                    "attachment": {
                        "payload": {
                            "elements": [
                                {
                                    "buttons": [
                                        {
                                            "block_names": ["Article"],
                                            "set_attributes": {
                                                "ArticleID": 1,
                                                "Page": 0,
                                            },
                                            "title": "TO MĚ ZAJIMÁ",
                                            "type": "show_block",
                                        },
                                        {
                                            "block_names": ["ArticleNotInterested"],
                                            "set_attributes": {"ArticleID": 1},
                                            "title": "To mě nezajímá",
                                            "type": "show_block",
                                        },
                                    ],
                                    "image_url": "https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/02/downuv_syndrom3_0.png",
                                    "title": "Downův syndrom je nejčastější vrozená vada. Napoví už tvar hlavy, zásadní roli hraje věk matky",
                                },
                                {
                                    "buttons": [
                                        {
                                            "block_names": ["Article"],
                                            "set_attributes": {
                                                "ArticleID": 2,
                                                "Page": 0,
                                            },
                                            "title": "TO MĚ ZAJIMÁ",
                                            "type": "show_block",
                                        },
                                        {
                                            "block_names": ["ArticleNotInterested"],
                                            "set_attributes": {"ArticleID": 2},
                                            "title": "To mě nezajímá",
                                            "type": "show_block",
                                        },
                                    ],
                                    "image_url": "https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/03/babis1.jpeg",
                                    "title": "Babiš nám slíbil očkování, místo toho chce dát vakcínu puberťákům. Nechá nás klidně umřít, říká Jarmila (72)",
                                },
                                {
                                    "title": "To mi stačí",
                                    "buttons": [
                                        {
                                            "type": "show_block",
                                            "block_names": ["Outro"],
                                            "title": "To mi stačí",
                                        }
                                    ],
                                },
                            ],
                            "image_aspect_ratio": "square",
                            "template_type": "generic",
                        },
                        "type": "template",
                    }
                }
            ]
        }


def test_introduction_existing_user(app: Flask) -> None:
    dsn = app.config["SQLALCHEMY_DATABASE_URI"]
    with psycopg2.connect(dsn=dsn) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO users(messenger_id) VALUES(%s)",
                (
                    ("user1",),
                    ("user2",),
                ),
            )
            cursor.executemany(
                "INSERT INTO score(user_id, score, date) VALUES(%s, %s, %s)",
                (
                    (1, 5, date.today().isoformat()),
                    (2, 3, date.today().isoformat()),
                ),
            )

    with app.test_client() as client:
        response = client.post(
            "/v1/introduction",
            json={"messenger user id": "user1", "first name": "Ferda"},
        )
        assert response.json == {
            "messages": [
                {
                    "quick_replies": [
                        {
                            "block_names": ["Articles"],
                            "title": "Jdeme na to",
                            "type": "show_block",
                        },
                        {
                            "block_names": ["Articles"],
                            "title": "Odběr",
                            "type": "show_block",
                        },
                    ],
                    "text": "Á, Ferda, vítej zpátky.\nAktuálně máš celkem 5 "
                    "bodů. Za poslední týden jsi získal 5 bodů.\n",
                }
            ]
        }


def test_get_article_v1_get(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/v1/articles/1/")
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {
                    "text": "Downův syndrom je nejčastější vrozená vada. Napoví už tvar hlavy, zásadní roli hraje věk matky"
                },
                {
                    "attachment": {
                        "payload": {
                            "url": "https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/02/downuv_syndrom3_0.png"
                        },
                        "type": "image",
                    }
                },
                {
                    "quick_replies": [
                        {
                            "block_names": ["Question"],
                            "set_attributes": {
                                "ArticleID": 1,
                                "Page": 0,
                                "QuestionID": 1,
                            },
                            "title": "Dál",
                            "type": "show_block",
                        },
                        {
                            "block_names": ["Articles"],
                            "title": "Pryč",
                            "type": "show_block",
                        },
                    ],
                    "text": "Downův syndrom patří k nejčastějším vrozeným syndromům dítěte. Jedná se o nejběžnější poruchu chromozomů a bývá také nejvíce rozpoznatelnou příčinou mentální...",
                },
            ]
        }


def test_article_not_interested(app: Flask) -> None:
    with app.test_client() as client:
        response = client.post(
            "/v1/articles/1/not-interested",
            json={"messenger user id": "some-messenger-id"},
        )
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {
                    "attachment": {
                        "payload": {
                            "elements": [
                                {
                                    "buttons": [
                                        {
                                            "block_names": ["Article"],
                                            "set_attributes": {
                                                "ArticleID": 2,
                                                "Page": 0,
                                            },
                                            "title": "TO MĚ ZAJIMÁ",
                                            "type": "show_block",
                                        },
                                        {
                                            "block_names": ["ArticleNotInterested"],
                                            "set_attributes": {"ArticleID": 2},
                                            "title": "To mě nezajímá",
                                            "type": "show_block",
                                        },
                                    ],
                                    "image_url": "https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/03/babis1.jpeg",
                                    "title": "Babiš nám slíbil očkování, místo toho chce dát vakcínu puberťákům. Nechá nás klidně umřít, říká Jarmila (72)",
                                },
                                {
                                    "title": "To mi stačí",
                                    "buttons": [
                                        {
                                            "type": "show_block",
                                            "block_names": ["Outro"],
                                            "title": "To mi stačí",
                                        }
                                    ],
                                },
                            ],
                            "image_aspect_ratio": "square",
                            "template_type": "generic",
                        },
                        "type": "template",
                    }
                }
            ]
        }


def test_get_question(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/articles/1/questions/1/")
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {
                    "quick_replies": [
                        {
                            "block_names": ["ShowTextTest"],
                            "set_attributes": {
                                "AnswerID": 1,
                                "ArticleID": 1,
                                "QuizID": 1,
                            },
                            "title": "cosi",
                            "type": "show_block",
                        },
                    ],
                    "text": "Kdo napsal clanek?",
                }
            ]
        }


def test_check_answer(app: Flask) -> None:
    with app.test_client() as client:
        response = client.post(
            "/articles/1/questions/1/answers/1/",
            json={"messenger user id": "some-messanger-id"},
        )
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {
                    "attachment": {
                        "payload": {
                            "buttons": [
                                {
                                    "title": "Chcete vědět víc?",
                                    "type": "web_url",
                                    "url": "https://www.ctidoma.cz/zdravi/downuv-syndrom-je-nejcastejsi-vrozena-vada-napovi-uz-tvar-hlavy-zasadni-roli-hraje-vek-matky",
                                },
                                {
                                    "block_names": ["Articles"],
                                    "set_attributes": {"ArticleID": 1},
                                    "title": "Další zprávy",
                                    "type": "show_block",
                                },
                            ],
                            "template_type": "button",
                            "text": "Trefa! Jde ti to. 👍\nDám ti 1 bod, celkem máš 1 bod.\nDnes jsi správně odpověděl 1 otázku, když dáš 3, zítra se ti body násobí 2x",
                        },
                        "type": "template",
                    }
                }
            ]
        }


def test_check_answer_double_score(app: Flask) -> None:
    dsn = app.config["SQLALCHEMY_DATABASE_URI"]
    yesterday = date.today() - timedelta(days=1)
    with psycopg2.connect(dsn=dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users(messenger_id) VALUES('some-messanger-id')"
            )
            cursor.execute(
                "INSERT INTO score(user_id, score, date) VALUES(%s, %s, %s)",
                (1, 5, yesterday.isoformat()),
            )
    with app.test_client() as client:
        response = client.post(
            "/articles/1/questions/1/answers/1/",
            json={"messenger user id": "some-messanger-id"},
        )
        assert response.status_code == 200

    with app.test_client() as client:
        response = client.post(
            "/articles/1/questions/1/answers/1/",
            json={"messenger user id": "some-messanger-id"},
        )

    with psycopg2.connect(dsn=dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT score FROM score WHERE date = %s", (date.today().isoformat(),)
            )
            data = cursor.fetchone()
            assert data[0] == 4


def test_mocktext(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/mocktext")
        assert response.status_code == 200
        assert response.json == {
            "messages": [
                {"text": "Welcome to the Chatfuel Rockets!"},
                {"text": "What are you up to?"},
            ],
        }


def test_mockimage(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/mockimage")
        assert response.status_code == 200
        assert response.json == {
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


def test_mockfeed(app: Flask, monkeypatch) -> None:
    monkeypatch.setattr(feedparser, "parse", lambda x: {"feed": {"title": "ČtiDoma"}})

    with app.test_client() as client:
        response = client.get("/mockfeed")
        assert response.status_code == 200
        assert response.json == {"title": "ČtiDoma"}
