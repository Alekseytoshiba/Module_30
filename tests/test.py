import pytest
from factory.alchemy import SQLAlchemyModelFactory
from flask import Flask

from ..app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.String(20))


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session_persistence = "commit"

    name = "TestName"
    surname = "TestSurname"
    card_number = "1234567812345678"


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client_factory(app):
    with app.app_context():
        ClientFactory._meta.sqlalchemy_session = db.session
        yield ClientFactory
        db.session.rollback()


def test_client_creation_with_factory(app, client_factory):
    with app.app_context():
        initial_count = db.session.query(Client).count()
        client = client_factory()

        assert client.id is not None
        assert db.session.query(Client).count() == initial_count + 1
        assert client.name == "TestName"
        assert client.surname == "TestSurname"
        assert client.card_number == "1234567812345678"
