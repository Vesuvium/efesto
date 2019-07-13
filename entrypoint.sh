#!/bin/sh
efesto install;

if [ ! -z $ADMIN_NAME ]; then
    efesto create users $ADMIN_NAME --superuser
fi

if [ ! -z "$BLUEPRINT" ]; then
    echo "$BLUEPRINT" > blueprint.yml;
    efesto load blueprint.yml;
fi

gunicorn "efesto.App:App.run()" -b :5000
