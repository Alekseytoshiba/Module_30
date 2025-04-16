from flask import Blueprint, jsonify, request
from datetime import datetime
from ..models import db, Client, Parking, ClientParking

# Создание Blueprint для обработки запросов, связанных с парковкой клиентов
client_parkings_bp = Blueprint('client_parkings', __name__)


@client_parkings_bp.route('/client_parkings', methods=['POST'])
def park_car() -> tuple:
    """
    Обработка запроса на парковку автомобиля клиента.

    :return: JSON-объект с информацией о парковке или сообщение об ошибке.
    """
    # Получение данных из запроса
    data = request.get_json()

    # Проверка наличия необходимых данных в запросе
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return {'error': 'client_id and parking_id are required'}, 400

    # Получение клиента и парковки по их ID
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    # Проверка доступности парковки
    if not parking.is_open:
        return {'error': 'Parking is closed'}, 400
    if parking.free_spaces <= 0:
        return {'error': 'No available spaces'}, 400
    if not client.card_number:
        return {'error': 'Client has no payment card'}, 400

    # Уменьшение количества свободных мест на парковке
    parking.free_spaces -= 1

    # Создание записи о парковке клиента
    client_parking = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        entry_time=datetime.utcnow()
    )

    # Добавление записи в базу данных
    db.session.add(client_parking)
    db.session.commit()

    # Возвращение информации о парковке в формате JSON
    return jsonify(client_parking.to_dict()), 201


@client_parkings_bp.route('/client_parkings', methods=['DELETE'])
def leave_parking() -> tuple:
    """
    Обработка запроса на выход клиента из парковки.

    :return: JSON-объект с информацией о парковке или сообщение об ошибке.
    """
    # Получение данных из запроса
    data = request.get_json()

    # Проверка наличия необходимых данных в запросе
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return {'error': 'client_id and parking_id are required'}, 400

    # Получение клиента и парковки по их ID
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    # Поиск активной записи о парковке клиента
    client_parking = ClientParking.query.filter_by(
        client_id=client.id,
        parking_id=parking.id,
        exit_time=None
    ).first()

    # Проверка наличия активной парковки
    if not client_parking:
        return {'error': 'No active parking found'}, 400

    # Установка времени выхода из парковки
    client_parking.exit_time = datetime.utcnow()

    # Увеличение количества свободных мест на парковке
    parking.free_spaces += 1

    # Сохранение изменений в базе данных
    db.session.commit()

    # Возвращение информации о парковке в формате JSON
    return jsonify(client_parking.to_dict())
