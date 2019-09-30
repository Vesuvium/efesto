# Efesto

[![Pypi](https://img.shields.io/pypi/v/efesto.svg?maxAge=600&style=for-the-badge)](https://pypi.python.org/pypi/efesto)
[![Travis build](https://img.shields.io/travis/strangemachines/efesto.svg?maxAge=600&style=for-the-badge)](https://travis-ci.org/strangemachines/efesto)
[![Codacy grade](https://img.shields.io/codacy/grade/9a18a3f98f654fef8b6ff86e93f31b56.svg?style=for-the-badge)](https://app.codacy.com/app/strangemachines/efesto)
[![Codacy coverage](https://img.shields.io/codacy/coverage/9a18a3f98f654fef8b6ff86e93f31b56.svg?style=for-the-badge)](https://app.codacy.com/app/strangemachines/efesto)
[![Docs](https://img.shields.io/badge/docs-docs-brightgreen.svg?style=for-the-badge&cacheSeconds=3600)](https://efesto.strangemachines.io)

A micro REST API meant to be used almost out of the box with other
microservices.

It kickstarts you by providing a simple way to build a backend and expose it.
Efesto uses PostgreSQL and JWTs for authentication.

Efesto follows the UNIX principle of doing one thing and well, leaving you the
freedom of choice about other components (authentication, caching, rate-limiting,
load balancer).

## Installing
Install efesto, possibly in a virtual environment:

```sh
pip install efesto
```

Create a postgresql database and export the database url:

```sh
export DB_URL=postgres://postgres:postgres@localhost:5432/efesto
```

Export the jwt secret:

```sh
export JWT_SECRET=secret
```

Populate the db:

```sh
efesto install
```

Create an admin:

```sh
efesto create users tofu --superuser
```

Now you can start efesto, with either uwsgi or gunicorn:

```sh
gunicorn "efesto.App:App.run()"
```

Efesto should now be running:


```sh
curl http://localhost:8000/version
```

Read the complete [documentation](http://efesto.strangemachines.io) to find out more.

## Docker

Docker images are available in the hub:

- `strangemachines/efesto:latest`
- `strangemachines/efesto:2.3`
- `strangemachines/efesto:2.2`
- `strangemachines/efesto:2.1`

## Performance

Efesto performs at about 200 requests/second on a small digital ocean
droplet, for requests that include JWT authentication, fetching data and
printing out JSON.

You have seen 100k requests benchmarks, but don't be fooled:
most benchmarks from authors are made so that their package comes to the top
and do not reflect real conditions.
