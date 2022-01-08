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
1. Je třeba vytvořit chatfuel chatbot podle zadání v https://github.com/nfnz/newschatbot/blob/master/Chatfuel%20documentation.docx, případně se lze inspirovat v https://dashboard.chatfuel.com/bot/608e9a40c335e4231249d6b9/flows/608ed607c335e42312842da0 (a https://m.me/105203808395233)
3. Upravit v jednotlivých blocích URL na API podle toho, kde je nasazený backend. V našem případě je to např. https://v1r0yf8r51.execute-api.eu-west-3.amazonaws.com/dev/v1/<APIname>

## Newschatbot backend

Python Flask REST API application to support Chatfuels Chatbot. Deployment is done with Serverless Framework to AWS Lambda. Application is connected to Postgres database.

### Infrastructure
Infrastructure for backend and database is setup by Terraform(IaaC), deployment is automated by github actions. (It is required to specify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY secrets in github.)
  
### Deployment

Newschatbot backend is deployed using Serverless framework, automated by github actions. Function definition is in serverless.yml .

### Init dev setup
Python  setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Database setup
```
cd dockers/postgres/
docker-compose up

set FLASK_APP=app/main:app;
flask db upgrade
```
Flask application is run from app/main.py

### Database migration
  
Creates a migration repository
```
flask db init 
```
Generates migration file based on the model.
```
flask db migrate
```
Performs migration in the db.
```
flask db update
```
AWS PostgreSQL Database is not accessible directly, VPN needs to be setup.


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
