import requests
from newschatbot.app.config import FEED_URL
from newschatbot.app.model import metadata,  Article, Questions, Answers

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import xmltodict

# maybe how to use in serverless? https://stackoverflow.com/questions/61960140/serverless-how-to-periodically-run-a-flask-command-in-a-aws-lambda-function


def download_data_from_url():
    try:
        response = requests.get(FEED_URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    data = xmltodict.parse(response.content)
    return data


def update_articles():
    articles = download_data_from_url()
    for key, value in articles.items():
        for node, article_data in value.items():
            for q in article_data:
                exist = session.query(Article).filter_by(article_id=q['ID']).all()
                if not exist:
                    new_article = Article(article_id=q['ID'], published_date=q['CREATED_DATE'], title=q['TITLE'],
                                          creator=q['AUTHOR'], image_src=q['IMAGE'], link_src=q['LINK'],
                                          text=q['PEREX'],
                                          keywords='TODO', media_name='cti-doma')
                    session.add(new_article)
                    session.commit()

                    # TODO more than one question?
                    # TODO resolve FK issue

                    new_question = Questions(news_id=q['ID'], question_text=q['QUIZ']['QUIZ_TITLE'],
                                             question_type=1, order=order + 1)
                    session.add(new_question)
                    session.commit()

                    questions_id =session.query(Questions).filter_by(news_id=q['ID']).first()
                    questions_id = questions_id.id

                    # TODO more than one answer?
                    order = 1
                    for key, answer in q['QUIZ']['QUIZ_OPTIONS'].items():
                        correct_answer = filter(lambda x: x['CORRECT'] == '1', answer)
                        for option in answer:
                            new_answer = Answers(question_id=questions_id,
                                                 answer_text=option['OPTION_LABEL'],
                                                 correct_answer_text= list(correct_answer)[0]['OPTION_LABEL'],
                                                 correct_answers=option['OPTION_LABEL'] if q['CORRECT'] == "1" else None,
                                                 order=order + 1)
                            session.add(new_answer)
                            session.commit()






if __name__ == '__main__':
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/feed_parser"
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session(engine)
    update_articles()

    session.close()