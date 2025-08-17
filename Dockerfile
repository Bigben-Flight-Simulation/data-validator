FROM python:3.10-slim

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/
RUN pip install poetry && poetry install

ENTRYPOINT ["poetry", "run", "data-validator"]
