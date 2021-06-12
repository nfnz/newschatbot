from flask import Flask
from flask_migrate import Migrate

from app.model import db
from app.controller import api

app = Flask(__name__)
app.register_blueprint(api)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://newschatbotdevelopment:Wlk8skrHKvZEbM6Gw@database.internal.newschatbot.ceskodigital.net:5432/newschatbotdevelopment"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/feed_parser"
migrate = Migrate(app, db)
db.init_app(app)


if __name__ == '__main__':
    app.run()
