from flask import Blueprint, jsonify, request
from ..models import db, Client

# Создание Blueprint для обработки запросов, связанных с клиентами
clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients', methods=['GET'])
def get_clients() -> tuple:
    """
    Получение списка всех клиентов.

    :return: JSON-список с информацией о клиентах.
    """
    # Получение всех клиентов из базы данных
    clients = Client.query.all()

    # Возвращение списка клиентов в формате JSON
    return jsonify([client.to_dict() for client in clients])


@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id: int) -> tuple:
    """
    Получение информации о клиенте по его ID.

    :param client_id: ID клиента.
    :return: JSON-объект с информацией о клиенте или сообщение об ошибке 404.
    """
    # Получение клиента по его ID
    client = Client.query.get_or_404(client_id)

    # Возвращение информации о клиенте в формате JSON
    return jsonify(client.to_dict())


@clients_bp.route('/clients', methods=['POST'])
def create_client() -> tuple:
    """
    Создание нового клиента.

    :return: JSON-объект с информацией о созданном клиенте или сообщение об ошибке.
    """
    # Получение данных из запроса
    data = request.get_json()

    # Проверка наличия необходимых данных в запросе
    if not data or 'name' not in data or 'surname' not in data:
        return {'error': 'Name and surname are required'}, 400

    # Создание нового клиента
    client = Client(
        name=data['name'],
        surname=data['surname'],
        card_number=data.get('card_number')
    )

    # Добавление клиента в базу данных
    db.session.add(client)
    db.session.commit()

    # Возвращение информации о созданном клиенте в формате JSON
    return jsonify(client.to_dict()), 201
