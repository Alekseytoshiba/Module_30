from app import create_app

app = create_app()

if __name__ == '__main__':
    """
    Точка входа программы.

    Если скрипт запущен непосредственно, запускается приложение в режиме отладки.
    """
    app.run(debug=True)



