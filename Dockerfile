FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

COPY src/ ./src/
COPY examples/ ./examples/

ENTRYPOINT ["poetry", "run", "data-validator"]
