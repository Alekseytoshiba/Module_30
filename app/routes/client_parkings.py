from datetime import datetime
from typing import Tuple, Union

from flask import Blueprint, Response, jsonify, request

from ..models import Client, ClientParking, Parking, db

client_parkings_bp = Blueprint("client_parkings", __name__)


@client_parkings_bp.route("/client_parkings", methods=["POST"])
def park_car() -> Union[Tuple[dict, int], Tuple[Response, int]]:
    """
    Обработка запроса на парковку автомобиля клиента.
    :return: JSON-объект с информацией о парковке или сообщение об ошибке.
    """
    data = request.get_json()

    if not data or "client_id" not in data or "parking_id" not in data:
        return {"error": "client_id and parking_id are required"}, 400

    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    if not parking.is_open:
        return {"error": "Parking is closed"}, 400
    if parking.free_spaces <= 0:
        return {"error": "No available spaces"}, 400
    if not client.card_number:
        return {"error": "Client has no payment card"}, 400

    parking.free_spaces -= 1
    client_parking = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        entry_time=datetime.utcnow(),
    )

    db.session.add(client_parking)
    db.session.commit()

    return jsonify(client_parking.to_dict()), 201


@client_parkings_bp.route("/client_parkings", methods=["DELETE"])
def leave_parking() -> Union[Tuple[dict, int], Tuple[Response, int]]:
    """
    Обработка запроса на выход клиента из парковки.
    :return: JSON-объект с информацией о парковке или сообщение об ошибке.
    """
    data = request.get_json()

    if not data or "client_id" not in data or "parking_id" not in data:
        return {"error": "client_id and parking_id are required"}, 400

    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    client_parking = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id, exit_time=None
    ).first()

    if not client_parking:
        return {"error": "No active parking found"}, 400

    client_parking.exit_time = datetime.utcnow()
    parking.free_spaces += 1
    db.session.commit()

    return jsonify(client_parking.to_dict()), 200
