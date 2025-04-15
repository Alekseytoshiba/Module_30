from typing import List, Dict, Any
from flask import Flask, jsonify
from .config import Config
from .models import db, Client, Parking, ClientParking


def create_app() -> Flask:
    """
    Функция инициализации приложения Flask.

    Возвращает:
        Flask: Объект приложения Flask.
    """
    app = Flask(__name__)
    """
    Создает экземпляр приложения Flask.
    Параметры:
        __name__: Имя текущего модуля.
    """
    app.config.from_object(Config)
    """
    Загружает конфигурационные параметры из класса Config.
    """

    db.init_app(app)
    """
    Инициализирует объект базы данных для работы с приложением Flask.
    """

    with app.app_context():
        db.create_all()

    @app.route('/clients', methods=['GET'])
    def get_clients() -> List[Dict[str, Any]]:
        """
        Маршрут для получения списка клиентов.

        Возвращает:
            list[dict]: Список клиентов в формате JSON.
        """
        clients = Client.query.all()

        return jsonify([
            {
                'id': client.id,
                'name': client.name,
                'surname': client.surname
            }
            for client in clients
        ])
    return app




