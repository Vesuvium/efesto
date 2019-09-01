#!/bin/sh
DB_URL=postgres://postgres:postgres@localhost:5432/efesto;

apt-get install python3 python3-pip postgres;
pip3 install efesto gunicorn gunicorn[tornado] gunicorn[gevent];
