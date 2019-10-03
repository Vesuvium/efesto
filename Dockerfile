FROM        python:3.7-slim

ARG server=gunicorn
ENV SERVER=$server

COPY . /app
WORKDIR /app

RUN     ./build.sh
RUN     poetry install --no-dev

ENTRYPOINT ["./entrypoint.sh"]
