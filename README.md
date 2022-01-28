## Idea Chatbota Newsie 
Zpravodajské články jen těžko obstojí v konkurenci zábavných obsahů sociálních sítí, her a interaktivních formátů. Zaujměte své čtenáře Chatbotem Newsie, který bude představovat zprávy postupně, bude se uživatele ptát a motivovat ho, aby se ke zprávám vracel.

## Inovace zpravodajského storytellingu 
Projekt vznikl ve spoluprácí Nadačního fondu nezávislé žurnalistiky a Česko.Digital. Cílem bylo navrhnout prototyp, který by dostat zpravodajství k lidem, kteří zprávy nečtou ([dle výzkumu](https://www.nfnz.cz/studie-a-analyzy/cesi-a-zpravodajstvi/) se jedná o více než 30 % populace). Zapojili jsme 150 expertních dobrovolníků a novináře z 10 redakcí. Ověřovali jsme si hypotézy, ptali se novinářů i mediálních domů. Idea chatbota zvítězila v konkurenci téměř stovky nápadů.

## Koncept v kostce
Chatbot funguje na platformě [Messenger](https://cs.wikipedia.org/wiki/Facebook_Messenger) a přináší informace o dění kolem lidem, kteří o ně mají sice zájem, ale zpravodajské servery pro ně nejsou vhodnou formou, nebo nemají čas, chuť či disciplínu zprávy sledovat. Chatbot funguje pro konkrétní redakci, která dodává obsah prostřednictvím RSS. Redakce získávají nové, především mladé čtenáře. Po přečtení zpráv si uživatel může udělat kvíz a získat body. Čtenář je motivován každý den číst alespoň 3 zprávy. 

<img width="1434" alt="obrazek" src="https://user-images.githubusercontent.com/69157075/150365703-8d299281-f401-4767-91a8-3adfbe927177.png">


# Jak to funguje
Koncept projektu, jeho přidanou hodnotu uživateli, cíl a benefity najdete v prezentaci [Chatbot Newsie](https://docs.google.com/presentation/d/1hS9tdPj9EITdcgzo-2qJ_53amQ4pWriF9H6l-a5WkCk/). 

## Licence
Projekt je open source, kdokoliv má právo kdykoliv využít dokumentaci pro své účely. Na projekt platí MIT license. Více MIT licenci naleznete na [popisu na GitHub](https://github.com/nfnz/newschatbot/blob/master/LICENSE).

## Návod pro spuštění v nové redakci
Redakce bude potřebovat provést 3 hlavní kroky:
  1) Vytvořit si profil v online platformě [Chatfuel](Chatfuel.com), která zprostředkovává chování chatbota v Messengeru.
  2) Druhým krokem bude spusti backend chatbota v jazyce Python.
  3) Následně je třeba propojit Chatfuel, backend a RSS redakce.

## Chatfuel
Online nástroj Chatfuel nabízí několik verzí, my používali verzi za 15$/měsíc. Zde si definujte workflow a bloky, které volají prostřednictvím API backend. V tomto nástroji nastavíte, jak bude chatbot na uživatele reagovat, jak mu bude zprávy zobrazovat a jaké otázky mu bude klást.
1. Nastavte si chatbota v Chatfuel podle následujícího [zadání](https://docs.google.com/document/d/18zOGlWSjJWydNlYczLIvLEuoPa8K857VnnpsQ0-8Bxo/edit?usp=sharing)
3. Upravte v jednotlivých blocích URL na API podle toho, kde je nasazený backend. Při tvorbě prototypu se jednalo např. o https://v1r0yf8r51.execute-api.eu-west-3.amazonaws.com/dev/v1/<APIname>

## Newschatbot backend

Python Flask REST API application to support Chatfuels Chatbot. Deployment is done with Serverless Framework to AWS Lambda. Application is connected to Postgres database.

### Infrastructure
Infrastructure for backend and database is setup by Terraform(IaaC), deployment is automated by github actions. (It is required to specify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY secrets in github.)

AWS PostgreSQL Database is not accessible directly, VPN needs to be setup. To get access please contact @martinwenisch
  
### Deployment

Newschatbot backend is deployed using Serverless framework, automated by github actions. Function definition is in serverless.yml .

### Local Deployment
**Launch the services with Docker Compose:**

```
docker-compose up
```
It starts the flask application, postgreSQL server and runs database migrations.

Can be tested with following:
```
curl http://127.0.0.1:5000/v1/articles/
```

### Development setup
**Python setup**

Project is meant to be run with Python 3.6

Creation of virtual environment and installation of dependencies. You might encounter problems with installing the `greenlet` module. (For Mac users please change greenlet==0.4.10 to greenlet==0.4.16 in requirements.txt) 
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Database setup**

Running PostgreSQL with Docker Compose: (Alternatively PostgreSQL can be downloaded at https://www.postgresql.org/download/)
```
cd dockers/postgres/
docker-compose up
```
**Database migration**, 

export environment variable FLASK_APP (use _export_ in linux instead of _set_)
```
set FLASK_APP=app/main:app;
```
export environment variable DB_CONNSTR (use _export_ in linux instead of _set_)
```
set DB_CONNSTR="postgresql://postgres:postgres@localhost:5432/feed_parser"
```
run the migration,
```
flask db upgrade
```
**Application start**
```
flask run
```
Flask application is run from app/main.py

### Database migration

Generates migration file based on the model (app/model.py).
```
flask db migrate
```
Performs migration in the db.
```
flask db update
```

### Contributing
#### Before pushing changes
Before you push your changes, run code formatter Black by using the following command:
```
black {source_file_or_directory} 
```
If the script doesn't work, run Black as package: 
```
python3 -m black {source_file_or_directory}
```
