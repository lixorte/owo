FROM node:alpine AS build

WORKDIR /app

COPY . .

RUN npm install --production

RUN npm run build

RUN ./deploy.sh

FROM alpine:edge

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apk add --no-cache python3 curl && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY --from=build /app/owo/ /app/owo/

CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:80", "owo.app:app"]