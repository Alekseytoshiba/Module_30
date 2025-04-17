class Config:
    """
    Класс для хранения конфигурационных настроек приложения.
    """

    # URI для подключения к базе данных SQLite
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///parking.db"

    # Выключение отслеживания изменений в базе данных
    # для улучшения производительности
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
