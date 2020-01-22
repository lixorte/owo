from node:alpine AS build

WORKDIR /app

COPY . .

RUN npm install --production

RUN npm run build

RUN ./deploy.sh

FROM alpine:edge

ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=build /app/owo/ /app/owo/

CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:80", "owo.app:app"]