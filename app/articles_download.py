import requests
import xmltodict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# original version had app.config and app.model. That wasn't working for me in local version
# but there might be different context when running on serverless, so might be worth a check
from config import FEED_URL
from model import Article, Questions, Answers


def download_data_from_url():
    try:
        response = requests.get(FEED_URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    data = xmltodict.parse(response.content)
    return data


def update_articles(session):
    articles = download_data_from_url()

    counter = 0
    for key, value in articles.items():
        for node, article_data in value.items():
            for q in article_data:
                exist = session.query(Article).filter_by(article_id=q["ID"]).all()
                if not exist:
                    counter = counter + 1
                    new_article = Article(
                        article_id=q["ID"],
                        published_date=q["CREATED_DATE"],
                        title=q["TITLE"],
                        creator=q["AUTHOR"],
                        image_src=q["IMAGE"],
                        link_src=q["LINK"],
                        text=q["PEREX"],
                        keywords="TODO",
                        media_name="cti-doma",
                    )
                    session.add(new_article)
                    session.commit()
                    session.refresh(new_article)

                    new_question = Questions(
                        news_id=new_article.id,
                        question_text=q["QUIZ"]["QUIZ_TITLE"],
                        question_type=1,
                        order=1,
                    )
                    session.add(new_question)
                    session.commit()
                    session.refresh(new_question)

                    order = 1  # tODO
                    for key, answer in q["QUIZ"]["QUIZ_OPTIONS"].items():
                        for option in answer:
                            new_answer = Answers(
                                question_id=new_question.id,
                                answer_text=option["OPTION_LABEL"],
                                correct_answer_text="TBD",
                                correct_answers=True
                                if option["CORRECT"] is not None
                                else False,
                                order=1,
                            )
                            session.add(new_answer)
                            session.commit()
    print(f"Added {counter} articles.")


def begin_import(event, context):
    # SQLALCHEMY_DATABASE_URI = "postgresql://newschatbotdevelopment:Wlk8skrHKvZEbM6Gw@database.internal.newschatbot.ceskodigital.net:5432/newschatbotdevelopment" #"postgresql://postgres:postgres@localhost:5432/db2" #"postgresql://postgres:postgres@localhost:5432/feed_parser"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost:5433/feed_parser"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session(engine)

    # disable FK constraints
    session.execute("SET session_replication_role = replica;")

    update_articles(session)

    # enable FK constraints
    session.execute("SET session_replication_role = DEFAULT;")

    session.close()


if __name__ == "__main__":
    begin_import(None, None)
