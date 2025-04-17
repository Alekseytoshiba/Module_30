from typing import Tuple, Union

from flask import Blueprint, Response, jsonify, request

from app import db

from ...app.models import Client

clients_bp = Blueprint("clients", __name__)


@clients_bp.route("/clients", methods=["GET"])
def get_clients() -> Union[Response, Tuple[Response, int]]:
    """
    Получение списка всех клиентов.
    :return: JSON-список с информацией о клиентах.
    """
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])


@clients_bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Получение информации о клиенте по его ID.
    :param client_id: ID клиента.
    :return: JSON-объект с информацией о клиенте или сообщение об ошибке 404.
    """
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict())


@clients_bp.route("/clients", methods=["POST"])
def create_client() -> Union[Response, Tuple[dict, int], Tuple[Response, int]]:
    """
    Создание нового клиента.
    :return: JSON-объект с информацией о созданном клиенте или
    сообщение об ошибке.
    """
    data = request.get_json()  # Теперь используется правильный request

    if not data or "name" not in data or "surname" not in data:
        return {"error": "Name and surname are required"}, 400

    client = Client(
        name=data["name"],
        surname=data["surname"],
        card_number=data.get("card_number"),
    )

    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201
