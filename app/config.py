import os


class Config:
    """
    Класс для хранения настроек приложения.

    Атрибуты:
        SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Отслеживание изменений в моделях.
    """
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    """
    Строка подключения к базе данных.
    По умолчанию использует SQLite базу данных `site.db`, если переменная окружения `DATABASE_URL` не установлена.
    """

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    """
    Опция отслеживания модификаций для SQLAlchemy.
    Устанавливается в False для повышения производительности.
    """



