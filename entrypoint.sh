#!/bin/sh
efesto install;

if [ ! -z $ADMIN_NAME ]; then
    efesto create-user $ADMIN_NAME --superuser
fi

if [ ! -z "$BLUEPRINT" ]; then
    echo "$BLUEPRINT" > blueprint.yml;
    efesto load-blueprint blueprint.yml;
    efesto generate;
fi

gunicorn "efesto.App:App.run()" -b :5000
