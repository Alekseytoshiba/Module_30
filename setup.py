from setuptools import setup, find_packages

setup(
    name="parking_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "pydantic",
        # другие зависимости
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "requests",
        ],
    },
)