import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from factory.alchemy import SQLAlchemyModelFactory

# Инициализация SQLAlchemy
db = SQLAlchemy()


# Модель Client
class Client(db.Model):
    """
    Модель для представления клиента.

    Атрибуты:
        id (int): Уникальный идентификатор клиента.
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        card_number (str): Номер карты клиента.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.String(20))


# Фабрика с явным сохранением в БД
class ClientFactory(SQLAlchemyModelFactory):
    """
    Фабрика для создания объектов модели Client.

    Атрибуты:
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        card_number (str): Номер карты клиента.

    Метаданные:
        model (Client): Модель, для которой создается фабрика.
        sqlalchemy_session (Session): Сессия SQLAlchemy для работы с базой данных.
        sqlalchemy_session_persistence (str): Настройка для автоматического коммита изменений.
    """
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"  # Автоматически коммитит изменения

    name = "TestName"
    surname = "TestSurname"
    card_number = "1234567812345678"


@pytest.fixture
def app() -> Flask:
    """
    Фикстура для создания тестового приложения Flask.

    :return: Экземпляр тестового приложения.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


def test_client_creation_with_factory(app):
    """
    Тест создания клиента с помощью фабрики.

    Проверяет:
    - Генерацию ID клиента.
    - Увеличение количества клиентов в базе данных.
    - Соответствие атрибутов клиента значениям, заданным в фабрике.
    """
    with app.app_context():
        # Убедимся, что сессия установлена
        ClientFactory._meta.sqlalchemy_session = db.session

        initial_count = db.session.query(Client).count()
        client = ClientFactory()

        # Явно обновим сессию
        db.session.refresh(client)

        # Проверки
        assert client.id is not None, "ID клиента не был сгенерирован"
        assert db.session.query(Client).count() == initial_count + 1
        assert client.name == "TestName"
        assert client.surname == "TestSurname"
        assert client.card_number == "1234567812345678"
