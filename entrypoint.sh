#!/bin/sh
efesto install;

if [ ! -z $ADMIN_NAME ]; then
    efesto create users $ADMIN_NAME --superuser
fi

if [ ! -z "$BLUEPRINT" ]; then
    echo "$BLUEPRINT" > blueprint.yml;
    efesto load blueprint.yml;
fi

if [ ! $WORKERS ]; then
    WORKERS=3;
fi

if [ ! $WORKER_CLASS ]; then
    WORKER_CLASS=sync;
else
    pip install $WORKER_CLASS;
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

gunicorn "efesto.App:App.run()" -b :5000 -w $WORKERS -k $WORKER_CLASS \
        --threads $THREADS -t $TIMEOUT --graceful-timeout $TIMEOUT \
        --max-requests-jitter $JITTER
