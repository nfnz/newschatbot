FROM python:3.6.13-slim-buster

WORKDIR /appl/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app/main:app

RUN pip install --upgrade pip

COPY ./app /appl/app/

COPY ./requirements.txt /appl/requirements.txt
COPY ./migrations /appl/migrations
RUN pip install -r requirements.txt

EXPOSE 5000



