FROM python:3.10-slim

COPY pyproject.toml poetry.lock README.md ./
RUN pip install poetry && poetry install

COPY src/ ./src/

ENTRYPOINT ["poetry", "run", "data-validator"]
