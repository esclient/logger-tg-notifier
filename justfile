format:
    black .
    isort .
    ruff check . --fix

lint:
    black --check .
    isort . --check --diff
    flake8 .
    ruff check .
    mypy --strict .

test:
    pytest

prepare: format lint test
