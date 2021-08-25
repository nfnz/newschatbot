INSERT INTO articles(
    article_id,
    published_date,
    title,
    creator,
    image_src,
    link_src,
    text,
    keywords,
    media_name
)
VALUES
(
    65228,
    '5/3/21 5:00',
    'Downův syndrom je nejčastější vrozená vada. Napoví už tvar hlavy, zásadní roli hraje věk matky',
    'Martin Chalupa',
    'https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/02/downuv_syndrom3_0.png',
    'https://www.ctidoma.cz/zdravi/downuv-syndrom-je-nejcastejsi-vrozena-vada-napovi-uz-tvar-hlavy-zasadni-roli-hraje-vek-matky',
    'Downův syndrom patří k nejčastějším vrozeným syndromům dítěte. Jedná se o nejběžnější poruchu chromozomů a bývá také nejvíce rozpoznatelnou příčinou mentální...',
    'TODO',
    'cti-doma'
),
(
    65237,
    '5/3/21 4:42',
    'Babiš nám slíbil očkování, místo toho chce dát vakcínu puberťákům. Nechá nás klidně umřít, říká Jarmila (72)',
    'Karel Havránek',
    'https://www.ctidoma.cz/sites/default/files/styles/seznam/public/imgs/03/babis1.jpeg',
    'https://www.ctidoma.cz/politika/babis-nam-slibil-ockovani-misto-toho-chce-dat-vakcinu-pubertakum-necha-nas-klidne-umrit',
    'Slibem nezarmoutíš, řekl si zřejmě premiér Andrej Babiš, když 14. března ve svém internetovém pořadu Čau lidi slíbil, že od 6. dubna se v České republice každý...',
    'TODO',
    'cti-doma'
);

INSERT INTO questions(
    news_id,
    question_text,
    question_type,
    "order"
)
VALUES
(
    1,
    'Kdo napsal clanek?',
    1,
    1
);

INSERT INTO answers(
    question_id,
    answer_text,
    correct_answers,
    correct_answer_text,
    "order"
)
VALUES
(
    1,
    'cosi',
    true,
    'cosi',
    1
);