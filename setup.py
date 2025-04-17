from setuptools import find_packages, setup

setup(
    name="parking_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "Flask-SQLAlchemy>=3.0.0",
        "SQLAlchemy>=1.4.0",
        "factory_boy>=3.2.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "requests>=2.26.0",
        ],
        "dev": [
            "black>=22.0",
            "flake8>=4.0",
            "isort>=5.0",
            "mypy>=0.900",
        ],
    },
    python_requires=">=3.8",
)
