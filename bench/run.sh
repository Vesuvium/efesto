#!/bin/sh
DB_URL=postgres://postgres:postgres@localhost:5432/efesto;

gunicorn "efesto.App:App.run()" -b :5000 -w $3 -k $1 --threads $2 -t 60 \
    --graceful-timeout 60 --max-requests-jitter 60 --log-level ERROR -D
