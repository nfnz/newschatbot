import os

from flask import Flask
from flask_migrate import Migrate

from app.model import db
from app.controller import api

app = Flask(__name__)
app.register_blueprint(api)
db_connstr = os.environ.get('DB_CONNSTR', "postgresql://newschatbotdevelopment:Wlk8skrHKvZEbM6Gw@database.internal.newschatbot.ceskodigital.net:5432/newschatbotdevelopment")
app.config["SQLALCHEMY_DATABASE_URI"] = db_connstr
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)


if __name__ == "__main__":
    app.run()
