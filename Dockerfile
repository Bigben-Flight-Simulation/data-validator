FROM python:3.10-slim

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install

COPY src/ ./src/

ENTRYPOINT ["poetry", "run", "data-validator"]
