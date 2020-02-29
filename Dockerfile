FROM node:alpine AS build

WORKDIR /app

COPY . .

RUN npm install --production

RUN npm run build

RUN ./deploy.sh

FROM python:3.7.6-buster

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY . .

RUN poetry install --no-dev

CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:80", "owo.app:app"]