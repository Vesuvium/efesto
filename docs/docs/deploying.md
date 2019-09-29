# Deploying

The most common ways to deploy Efesto are by using a WSGI server of your choice
(suchs as gunicorn or uwsgi) or by using the available docker images.

If you are using a WSGI server, all you need to do is to set the options in the
enviroment.

## Docker-based deploy

Efesto can be found as docker image under `strangemachines/efesto`. The images
use gunicorn as WSGI server.

To facilitate docker-based deployments and allow passing options to gunicorn,
there are a number of additional environment options available.


### ADMIN_NAME

When given, a superuser with the given name will be created.

### BLUEPRINT

The BLUEPRINT environment variable is a way to pass to the efesto container
the blueprint that you want to use, instead of having to load that manually.

It's common to set this value with
`cat`: `export BLUEPRINT=$(cat <your-blueprint>)`

### PORT

The port on which gunicorn will run. Defaults to `:5000`

### WORKERS

How many workers should gunicorn use. Defaults to `3`.

### WORKER_CLASS

The class of the gunicorn workers. Defaults to `sync`.

When set, it will also install the worker with `pip install`.

### THREADS

How many threads should gunicorn use. Defaults to `1`.

### TIMEOUT

The timeout before a worker is restarted. It's passed to both `-t` and
`--graceful-timeout`. Defaults to `60`.

### JITTER

Gunicorn jitter to randomize workers timeout time. Defaults to `$WORKERS * 5`.
