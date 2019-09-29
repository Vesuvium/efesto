#!/bin/sh
poetry run efesto install;

if [ ! -z $ADMIN_NAME ]; then
    poetry run efesto create users $ADMIN_NAME --superuser
fi

if [ ! -z "$BLUEPRINT" ]; then
    echo "$BLUEPRINT" > blueprint.yml;
    poetry run efesto load blueprint.yml;
fi

if [ ! $PORT ]; then
    PORT=:5000
fi

if [ ! $WORKERS ]; then
    WORKERS=3;
fi

if [ ! $WORKER_CLASS ]; then
    WORKER_CLASS=sync;
else
    poetry run pip install $WORKER_CLASS;
fi

if [ ! $THREADS ]; then
    THREADS=1;
fi

if [ ! $TIMEOUT ]; then
    TIMEOUT=60;
fi

if [ ! $JITTER ]; then
    JITTER=$(( $WORKERS * 5 ));
fi

poetry run gunicorn "efesto.App:App.run()" -b $PORT -w $WORKERS \
        -k $WORKER_CLASS --threads $THREADS -t $TIMEOUT \
        --graceful-timeout $TIMEOUT --max-requests-jitter $JITTER
