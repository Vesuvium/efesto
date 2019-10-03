#!/bin/sh

if [ $SERVER = "meinheld" ]; then
    apt-get update;
    apt-get install -y --no-install-recommends gcc build-essential;
    rm -rf /var/lib/apt/lists;
fi

pip install poetry
poetry run pip install gunicorn

if [ $SERVER = "meinheld" ]; then
    poetry run pip install meinheld
    apt-get purge -y --auto-remove gcc build-essential
fi

