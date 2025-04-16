from flask import Blueprint, jsonify, request
from ..models import db, Parking

# Создание Blueprint для обработки запросов, связанных с парковками
parkings_bp = Blueprint('parkings', __name__)


@parkings_bp.route('/parkings', methods=['POST'])
def create_parking() -> tuple:
    """
    Создание новой парковки.

    :return: JSON-объект с информацией о созданной парковке или сообщение об ошибке.
    """
    # Получение данных из запроса
    data = request.get_json()

    # Проверка наличия необходимых данных в запросе
    if not data or 'name' not in data or 'total_spaces' not in data:
        return {'error': 'Name and total_spaces are required'}, 400

    # Создание новой парковки
    parking = Parking(
        name=data['name'],
        total_spaces=data['total_spaces'],
        free_spaces=data['total_spaces'],
        is_open=data.get('is_open', True)  # По умолчанию парковка открыта
    )

    # Добавление парковки в базу данных
    db.session.add(parking)
    db.session.commit()

    # Возвращение информации о созданной парковке в формате JSON
    return jsonify(parking.to_dict()), 201
