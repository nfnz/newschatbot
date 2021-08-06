from flask_sqlalchemy import SQLAlchemy

from app.model import metadata

db = SQLAlchemy(metadata=metadata)