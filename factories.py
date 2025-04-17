import random

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from .app import db
from .app.models import Client, Parking

# Инициализация Faker для генерации фейковых данных
fake = Faker()


class ClientFactory(SQLAlchemyModelFactory):
    """
    Фабрика для создания объектов модели Client.

    Атрибуты:
        name (str): Имя клиента (генерируется с помощью Faker).
        surname (str): Фамилия клиента (генерируется с помощью Faker).
        card_number (str): Номер карты клиента (генерируется случайно, может быть None).
    """

    class Meta:
        """
        Метаданные для фабрики.

        Атрибуты:
            model (Client): Модель, для которой создается фабрика.
            sqlalchemy_session (Session): Сессия SQLAlchemy для работы с базой данных.
        """

        model = Client
        sqlalchemy_session = db.session  # Используем сессию SQLAlchemy

    name = factory.Faker("first_name")  # Генерация имени
    surname = factory.Faker("last_name")  # Генерация фамилии
    # Карта может быть или не быть (50/50)
    card_number = factory.LazyAttribute(
        lambda x: fake.credit_card_number()
        if random.choice([True, False])
        else None
    )


class ParkingFactory(SQLAlchemyModelFactory):
    """
    Фабрика для создания объектов модели Parking.

    Атрибуты:
        name (str): Название парковки (генерируется как адрес с помощью Faker).
        is_open (bool): Флаг, указывающий, открыта ли парковка (генерируется случайно).
        total_spaces (int): Общее количество мест на парковке (генерируется случайно).
        free_spaces (int): Количество свободных мест на парковке (генерируется случайно, не больше общего количества).
    """

    class Meta:
        """
        Метаданные для фабрики.

        Атрибуты:
            model (Parking): Модель, для которой создается фабрика.
            sqlalchemy_session (Session): Сессия SQLAlchemy для работы с базой данных.
        """

        model = Parking
        sqlalchemy_session = db.session

    name = factory.Faker("street_address")  # Адрес как название парковки
    is_open = factory.Faker("boolean")  # Открыта или закрыта
    total_spaces = factory.Faker("random_int", min=10, max=1000)  # Всего мест
    # Свободные места (не больше общего количества)
    free_spaces = factory.LazyAttribute(
        lambda o: random.randint(0, o.total_spaces)
    )
