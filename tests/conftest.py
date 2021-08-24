from flask import Flask
from flask_migrate import Migrate
import psycopg2
import pytest
import pytest_docker
import tenacity

from app.model import db
from app.controller import api


def ensure_schema(dsn: str) -> None:
    with open("tests/data/schema.sql") as f:
        with psycopg2.connect(dsn=dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f.read())


def insert_data(dsn: str) -> None:
    with open("tests/data/db_data.sql") as f:
        with psycopg2.connect(dsn=dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f.read())


def delete_data(dsn: str) -> None:
    with psycopg2.connect(dsn=dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DROP TABLE answers;
                DROP TABLE questions;
                DROP TABLE score;
                DROP TABLE reading;
                DROP TABLE users;
                DROP TABLE articles;
                """
            )


@pytest.fixture(scope="session")
def postgres_dsn(docker_services: pytest_docker.plugin.Services) -> str:
    host = "127.0.0.1"
    port = docker_services.port_for("postgres", 5432)
    username = password = "postgres"
    database = "test"
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


@pytest.fixture(scope="session")
def pg_connection(postgres_dsn: str):
    @tenacity.retry(
        stop=tenacity.stop_after_delay(30),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(
            (
                psycopg2.Error,
                psycopg2.DatabaseError,
                psycopg2.OperationalError,
            )
        ),
    )
    def connect():
        return psycopg2.connect(dsn=postgres_dsn)

    connection = connect()
    return connection


@pytest.fixture(scope="session")
def app(pg_connection, postgres_dsn: str) -> Flask:
    app = Flask("app/main")
    app.register_blueprint(api)
    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_dsn
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    migrate = Migrate(app, db)
    db.init_app(app)
    ensure_schema(postgres_dsn)
    insert_data(postgres_dsn)
    yield app
    delete_data(postgres_dsn)
