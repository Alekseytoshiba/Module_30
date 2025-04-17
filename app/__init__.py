from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ..factories import ClientFactory, ParkingFactory
from .config import Config

db = SQLAlchemy()


def create_app() -> Flask:
    """
    Создание экземпляра Flask-приложения.

    :return: Экземпляр Flask-приложения.
    """
    # Создание нового экземпляра Flask-приложения
    app = Flask(__name__)

    # Загрузка конфигурации из объекта Config
    app.config.from_object(Config)

    # Инициализация объекта SQLAlchemy для приложения
    db.init_app(app)

    return app


def factories() -> dict:
    """
    Импорт и возврат словаря фабрик для создания объектов моделей.

    :return: Словарь фабрик для моделей 'Client' и 'Parking'.
    """

    # Возвращение словаря с фабриками
    return {"Client": ClientFactory, "Parking": ParkingFactory}
