#!/bin/sh
if [ ! -f bombardier ]; then
    wget https://github.com/codesenberg/bombardier/releases/download/v1.2.4/bombardier-linux-amd64 -O bombardier;
fi

chmod 744 bombardier;

./bombardier $1/version -c 1000 -d 300s;
./bombardier $1/users -c 1000 -d 300s-H "Authorization: Bearer $2";
