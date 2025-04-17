import os
import sys

from git import Repo
from github import Github


def get_github_token():
    """Безопасный ввод токена GitHub с проверкой"""
    if "GITHUB_TOKEN" in os.environ:
        return os.environ["GITHUB_TOKEN"]

    try:
        import getpass

        token = getpass.getpass("Введите GitHub токен: ")
        if not token:
            raise ValueError("Токен не может быть пустым")
        return token
    except Exception as e:
        print(f"Ошибка ввода токена: {e}")
        sys.exit(1)


def upload_to_github(
    repo_path, github_token, repo_name, commit_message="Initial commit"
):
    try:
        # Инициализация репозитория
        if not os.path.exists(os.path.join(repo_path, ".git")):
            repo = Repo.init(repo_path)
            print(f"Инициализирован новый репозиторий в {repo_path}")
        else:
            repo = Repo(repo_path)
            print(f"Найден существующий репозиторий в {repo_path}")

        # Добавление файлов
        repo.git.add(A=True)
        if repo.index.diff("HEAD"):
            repo.index.commit(commit_message)
            print(f"Создан коммит: '{commit_message}'")
        else:
            print("Нет изменений для коммита.")
            return

        # Подключение к GitHub
        g = Github(github_token)

        # Проверка существования репозитория
        try:
            remote_repo = g.get_repo(repo_name)
            print(f"Репозиторий {repo_name} уже существует")
        except Exception:
            # Создание нового репозитория
            if "/" in repo_name:
                username, repo_name = repo_name.split("/")
                user = g.get_user(username)
                remote_repo = user.create_repo(repo_name, private=False)
            else:
                remote_repo = g.get_user().create_repo(repo_name, private=False)
            print(f"Создан новый репозиторий: {repo_name}")

        # Настройка origin и отправка
        if "origin" not in [remote.name for remote in repo.remotes]:
            origin = repo.create_remote(
                "origin", f"https://{github_token}@github.com/{repo_name}.git"
            )
        else:
            origin = repo.remotes.origin

        origin.push("HEAD:main", force=True)
        print("✅ Код успешно отправлен на GitHub!")

    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Настройки
    PROJECT_PATH = os.getcwd()
    REPO_NAME = input("Введите название репозитория (формат: username/repo): ").strip()
    COMMIT_MESSAGE = (
        input("Введите сообщение коммита [по умолчанию: 'Обновление кода']: ").strip()
        or "Обновление кода"
    )

    # Получение токена
    GITHUB_TOKEN = get_github_token()

    # Запуск процесса
    upload_to_github(PROJECT_PATH, GITHUB_TOKEN, REPO_NAME, COMMIT_MESSAGE)
