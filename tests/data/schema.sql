CREATE TABLE IF NOT EXISTS articles(
    id SERIAL PRIMARY KEY,
    article_id INTEGER,
    published_date TIMESTAMP,
    title VARCHAR,
    creator VARCHAR,
    image_src VARCHAR,
    link_src VARCHAR,
    text VARCHAR,
    keywords VARCHAR,
    media_name VARCHAR
);

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    messenger_id VARCHAR,
    keywords VARCHAR
);

CREATE TABLE IF NOT EXISTS reading(
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    user_id INTEGER REFERENCES users(id),
    attention INTEGER,
    "like" INTEGER,
    refused INTEGER,
    read INTEGER,
    score INTEGER
);

CREATE TABLE IF NOT EXISTS score(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_word VARCHAR,
    score INTEGER,
    date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions(
    id SERIAL PRIMARY KEY,
    news_id INTEGER REFERENCES articles(id),
    question_text VARCHAR,
    question_type INTEGER,
    "order" INTEGER
);

CREATE TABLE IF NOT EXISTS answers(
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id),
    answer_text VARCHAR,
    correct_answers BOOLEAN,
    correct_answer_text VARCHAR,
    "order" INTEGER
);
