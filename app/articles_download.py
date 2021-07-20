import requests
from newschatbot.app.config import FEED_URL
from newschatbot.app.model import Article, db, Questions, Answers
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
        print(value)
        order = 0
        for node, article_data in value.items():
            for q in article_data:
                exist = Article.query.filter_by(article_id=q['ID']).first()
                if not exist:
                    new_article = Article(article_id=q['ID'], published_date=q['CREATED_DATE'], title=q['TITLE'],
                                          creator=q['AUTHOR'], image_src=q['IMAGE'], link_src=q['LINK'],
                                          text=q['PEREX'],
                                          keywords='TODO', media_name='cti-doma')
                    db.session.add(new_article)
                    new_question = Questions(news_id=q['ID'], question_text=q['QUIZ']['QUIZ_TITLE'],
                                             question_type='basic', order=order + 1)
                    db.session.add(new_question)
                    db.session.commit()

                    questions_id = Questions.query.filter_by(news_id=q['ID']).first()
                    questions_id = questions_id.id
                    new_answer = Answers(question_id=questions_id,
                                         answer_text=q['QUIZ']['QUIZ_OPTIONS']['QUIZ_OPTION'][0]['OPTION_LABEL'],
                                         correct_answers=q['QUIZ']['QUIZ_OPTIONS']['QUIZ_OPTION'][0]['CORRECT'],
                                         order=order + 1)
                    db.session.add(new_answer)
                    db.session.commit()
