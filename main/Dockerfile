FROM python:3.10.5-slim-buster

ARG DB
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY pyproject.toml .
COPY wait-for-it.sh .
COPY . .
RUN chmod +x wait-for-it.sh
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --extras ${DB} --no-interaction --no-ansi
