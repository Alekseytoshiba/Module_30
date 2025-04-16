from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Инициализация объекта SQLAlchemy для работы с базой данных
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
    # Импорт фабрик для моделей Client и Parking
    from module_29_testing.hw.Задание_4.factories import ClientFactory, ParkingFactory

    # Возвращение словаря с фабриками
    return {
        'Client': ClientFactory,
        'Parking': ParkingFactory
    }
