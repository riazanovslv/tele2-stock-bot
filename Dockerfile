FROM python:3.8-alpine

ENV POETRY_VERSION=1.0.9 \
    PATH="/root/.poetry/bin:${PATH}"

WORKDIR /locust
COPY pyproject.toml poetry.lock ./

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk --no-cache add \
       g++ \
       zeromq-dev \
       curl \
       libffi-dev \
       make \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py | python \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && adduser -h / -s /bin/false -H -D tele2bot

COPY . .

USER tele2bot
ENTRYPOINT ["./entrypoint.sh"]
