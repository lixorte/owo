FROM node:alpine AS build

WORKDIR /app

ADD . .

RUN npm install --production

RUN npm run build

FROM python:3.7.6-buster

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry install --no-dev

COPY --from=build /app/owo/static /app/owo/static

COPY . .

CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:80", "owo.app:app"]