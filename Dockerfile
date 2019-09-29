FROM        python:3.7-slim

COPY . /app
WORKDIR /app

RUN     pip install poetry
RUN     poetry run pip install gunicorn
RUN     poetry install --no-dev

ENTRYPOINT ["./entrypoint.sh"]
