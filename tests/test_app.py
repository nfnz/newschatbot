from flask import Flask
import feedparser


# TODO: is test_get_articles_v1_post necessary?
def test_get_articles_v1_get(app: Flask) -> None:
    with app.test_client() as client:
        response = client.get("/v1/articles/")
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
                            ],
                            "image_aspect_ratio": "square",
                            "template_type": "generic",
                        },
                        "type": "template",
                    }
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
                    "text": "Downův syndrom patří k nejčastějším vrozeným syndromům dítěte. Jedná se o nejběžnější poruchu chromozomů a bývá také nejvíce rozpoznatelnou příčinou mentální..."
                },
                {
                    "quick_replies": [
                        {
                            "block_names": ["Question"],
                            "set_attributes": {
                                "ArticleID": 1,
                                "Like": 1,
                                "Page": 0,
                                "QuestionID": 1,
                            },
                            "title": "super",
                            "type": "show_block",
                        },
                        {
                            "block_names": ["Question"],
                            "set_attributes": {
                                "ArticleID": 1,
                                "Page": 0,
                                "QuestionID": 1,
                            },
                            "title": "ok",
                            "type": "show_block",
                        },
                        {
                            "block_names": ["Articles"],
                            "title": "nuda",
                            "type": "show_block",
                        },
                    ],
                    "text": "Článek je",
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
                                }
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
                        {
                            "title": "přejít " "na " "článek",
                            "type": "web_url",
                            "url": "https://www.ctidoma.cz/zdravi/downuv-syndrom-je-nejcastejsi-vrozena-vada-napovi-uz-tvar-hlavy-zasadni-roli-hraje-vek-matky",
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
                            "text": "Trefa! Pokud se chcete dozvědět víc, koukněte na článek:",
                        },
                        "type": "template",
                    }
                }
            ]
        }


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
