from datetime import datetime

from ..app import db


class Client(db.Model):
    """
    Модель для представления клиента.

    Атрибуты:
        id (int): Уникальный идентификатор клиента.
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        card_number (str): Номер карты клиента (необязательно).

    Методы:
        to_dict(): Возвращает словарь с информацией о клиенте.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.String(20))

    def to_dict(self) -> dict:
        """
        Преобразование объекта клиента в словарь.

        :return: Словарь с информацией о клиенте.
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "card_number": self.card_number,
        }


class Parking(db.Model):
    """
    Модель для представления парковки.

    Атрибуты:
        id (int): Уникальный идентификатор парковки.
        name (str): Название парковки.
        total_spaces (int): Общее количество мест на парковке.
        free_spaces (int): Количество свободных мест на парковке.
        is_open (bool): Флаг, указывающий,
        открыта ли парковка (по умолчанию True).

    Методы:
        to_dict(): Возвращает словарь с информацией о парковке.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_spaces = db.Column(db.Integer, nullable=False)
    free_spaces = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, default=True)

    def to_dict(self) -> dict:
        """
        Преобразование объекта парковки в словарь.

        :return: Словарь с информацией о парковке.
        """
        return {
            "id": self.id,
            "name": self.name,
            "total_spaces": self.total_spaces,
            "free_spaces": self.free_spaces,
            "is_open": self.is_open,
        }


class ClientParking(db.Model):
    """
    Модель для представления парковки клиента.

    Атрибуты:
        id (int): Уникальный идентификатор парковки клиента.
        client_id (int): Идентификатор клиента.
        parking_id (int): Идентификатор парковки.
        entry_time (datetime): Время въезда клиента на парковку.
        exit_time (datetime): Время выезда клиента
        с парковки (необязательно).

    Методы:
        to_dict(): Возвращает словарь с информацией о парковке клиента.
    """

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime)

    def to_dict(self) -> dict:
        """
        Преобразование объекта парковки клиента в словарь.

        :return: Словарь с информацией о парковке клиента.
        """
        return {
            "id": self.id,
            "client_id": self.client_id,
            "parking_id": self.parking_id,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
        }
