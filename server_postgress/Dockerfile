FROM python:3.10.5-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .