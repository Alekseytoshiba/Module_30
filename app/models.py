from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class Client(db.Model):
    """
    Модель клиента парковки.

    Атрибуты:
        id (int): Уникальный идентификатор клиента.
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        credit_card (Optional[str]): Номер кредитной карты клиента.
        car_number (Optional[str]): Номер автомобиля клиента.
    """
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """Уникальный идентификатор клиента."""

    name = db.Column(db.String(50), nullable=False)
    """Имя клиента."""

    surname = db.Column(db.String(50), nullable=False)
    """Фамилия клиента."""

    credit_card = db.Column(db.String(50))
    """Номер кредитной карты клиента."""

    car_number = db.Column(db.String(10))
    """Номер автомобиля клиента."""

    def __repr__(self) -> str:
        return f'<Client {self.name} {self.surname}>'


class Parking(db.Model):
    """
    Модель парковки.

    Атрибуты:
        id (int): Уникальный идентификатор парковки.
        address (str): Адрес парковки.
        opened (bool): Признак открытости парковки.
        count_places (int): Общее количество парковочных мест.
        count_available_places (int): Количество свободных парковочных мест.
    """
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """Уникальный идентификатор парковки."""

    address = db.Column(db.String(100), nullable=False)
    """Адрес парковки."""

    opened = db.Column(db.Boolean)
    """Признак открытости парковки."""

    count_places = db.Column(db.Integer, nullable=False)
    """Общее количество парковочных мест."""

    count_available_places = db.Column(db.Integer, nullable=False)
    """Количество свободных парковочных мест."""

    def __repr__(self) -> str:
        return f'<Parking {self.address}, available places: {self.count_available_places}>'


class ClientParking(db.Model):
    """
    Модель связи между клиентом и парковкой.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        client_id (int): Идентификатор клиента.
        parking_id (int): Идентификатор парковки.
        time_in (datetime): Время въезда на парковку.
        time_out (Optional[datetime]): Время выезда с парковки.
    """
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """Уникальный идентификатор записи."""

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id'),
        nullable=False
    )
    """Идентификатор клиента."""

    parking_id = db.Column(
        db.Integer,
        db.ForeignKey('parking.id'),
        nullable=False
    )
    """Идентификатор парковки."""

    time_in = db.Column(db.DateTime, default=datetime.utcnow)
    """Время въезда на парковку."""

    time_out = db.Column(db.DateTime)
    """Время выезда с парковки."""

    # Связи с моделями
    client = relationship("Client")
    parking = relationship("Parking")

    # Уникальное ограничение
    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    def __repr__(self) -> str:
        return f'<ClientParking client={self.client_id}, parking={self.parking_id}, time_in={self.time_in}, time_out={self.time_out}>'



