# Projekt: Inovace zpravodajského storytellingu 
Tento projekt vznikl ve spoluprácí NFNZ a Česko.Digital. Cílem je dostat zpravodajctví k lidem, kteří jsou dnes zcela mimo dosah (více než 30% populace). 
Vychází ze studie: https://www.nfnz.cz/studie-a-analyzy/cesi-a-zpravodajstvi/

Chatbot přináší kvalitní informace lidem, kteří o ně mají sice zájem, ale zpravodajské servery pro ně nejsou vhodnou formou, nebo nemají čas, chuť či disciplínu zprávy sledovat. Chatbot u'funguje pro konkrétní redakci, která dodává obsah prostřednictvím RSS. Redakce díky aplikaci získávají nové čtenáře. Po přečtení zpráv si uživatel může udělat kvíz a získat body. Čtenář je motivován každý den číst alespoň 3 zprávy. 

## Jak to funguje
Koncept projektu, jeho přidanou hodnotu uživateli, cíl a benefity najdete v prezentaci: https://docs.google.com/presentation/d/1hS9tdPj9EITdcgzo-2qJ_53amQ4pWriF9H6l-a5WkCk/

# Licence
MIT license - https://github.com/nfnz/newschatbot/blob/master/LICENSE

# Návod pro spuštění v nové redakci
Aplikace používá Chatfuel.com a backend v Python. V Chatfuel je definované workflow a bloky, které volají prostřednictvím API backend.

## Chatfuel
Abyste nastavili chování chatbota tak, jak jsme ho v tomto projektu navrhli, je třeba využít nástroje Chatfuel.com. V tomto nástroji nastavíte, jak bude chatbot na uživatele reagovat, jak mu bude zprávy zobrazovat a jaké otázky mu bude klást.
1. Je třeba nastavit si chatbot v Chatfuel podle následujícího zadání v https://github.com/nfnz/newschatbot/blob/master/Chatfuel%20documentation.docx, případně se lze inspirovat v https://dashboard.chatfuel.com/bot/608e9a40c335e4231249d6b9/flows/608ed607c335e42312842da0 (a https://m.me/105203808395233)
3. Upravit v jednotlivých blocích URL na API podle toho, kde je nasazený backend. V našem případě je to např. https://v1r0yf8r51.execute-api.eu-west-3.amazonaws.com/dev/v1/<APIname>

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

Creation of virtual environment and installation of dependencies. You might encounter problems with installing the `greenlet` module. Mac users might need to edit `requirements.txt` and change `greenlet==0.4.10` to `greenlet==0.4.16`. Also, if you are using Python 3.10 you might need to change `greenlet==0.4.10` to `greenlet==1.1`.
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
