from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import ForeignKey

from app import db

# Инициализация db с аннотацией типа
# db: SQLAlchemy = SQLAlchemy()


class Client(db.Model):  # type: ignore
    """
    Модель для представления клиента.
    """

    __tablename__ = 'client'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    surname: str = db.Column(db.String(50), nullable=False)
    card_number: Optional[str] = db.Column(db.String(20))

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта клиента в словарь.
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "card_number": self.card_number,
        }


class Parking(db.Model):  # type: ignore[name-defined]
    """
    Модель для представления парковки.
    """

    __tablename__ = 'parking'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    total_spaces: int = db.Column(db.Integer, nullable=False)
    free_spaces: int = db.Column(db.Integer, nullable=False)
    is_open: bool = db.Column(db.Boolean, default=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта парковки в словарь.
        """
        return {
            "id": self.id,
            "name": self.name,
            "total_spaces": self.total_spaces,
            "free_spaces": self.free_spaces,
            "is_open": self.is_open,
        }


class ClientParking(db.Model):  # type: ignore[name-defined]
    """
    Модель для представления парковки клиента.
    """

    __tablename__ = 'client_parking'

    id: int = db.Column(db.Integer, primary_key=True)
    client_id: int = db.Column(db.Integer, ForeignKey('client.id'))
    parking_id: int = db.Column(db.Integer, ForeignKey('parking.id'))
    entry_time: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time: Optional[datetime] = db.Column(db.DateTime)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта парковки клиента в словарь.
        """
        return {
            "id": self.id,
            "client_id": self.client_id,
            "parking_id": self.parking_id,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat()
            if self.exit_time
            else None,
        }
