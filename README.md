# Efesto

[![Pypi](https://img.shields.io/pypi/v/efesto.svg?maxAge=600&style=for-the-badge)](https://pypi.python.org/pypi/efesto)
[![Travis build](https://img.shields.io/travis/getefesto/efesto.svg?maxAge=600&style=for-the-badge)](https://travis-ci.org/getefesto/efesto)
[![Codacy grade](https://img.shields.io/codacy/grade/f7e53f5fa09043a48a52eee5a706c684.svg?style=for-the-badge)](https://app.codacy.com/app/getefesto/efesto)
[![Codacy grade](https://img.shields.io/codacy/coverage/f7e53f5fa09043a48a52eee5a706c684.svg?style=for-the-badge)](https://app.codacy.com/app/getefesto/efesto)

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
export db_url=postgres://postgres:postgres@localhost:5432/efesto
```

Export the jwt secret:

```sh
export jwt_secret=secret
```

Populate the db:

```sh
efesto quickstart
```

Create an admin:

```sh
efesto create_user tofu --superuser
```

Now you can start efesto, with either uwsgi or gunicorn:

```sh
gunicorn "efesto.App:App.run()"
```

Efesto should now be running, let's make sure it is. Create a jwt with the secret
you have configured. Efesto comes with an helper for that:

```
efesto token tofu 1000
```

Send a request with the token:

```sh
curl http://localhost:8000/users -H "Authorization: Bearer token"
```

Success! Efesto is running fine. Read the complete
`documentation <http://efesto.readthedocs.io>`_  to find out more

## Performance

Efesto performs at about 200 requests/second on a small digital ocean
droplet, for requests that include JWT authentication, fetching data and
printing out JSON.

You have seen 100k requests benchmarks, but don't be fooled:
most benchmarks from authors are made so that their package comes to the top
and do not reflect real conditions.

That said, Efesto's did not reach its maximum and a lot can be done to improve
its performance.


## Notes from the author

- Efesto is not meant to be the solution to all problems. It can be quite good
  as a prototyping and early stage backend, less so on the long term (see below)

- Efesto lacks some strategic features and I can only put a limited amount
  of time into Efesto. If you want some features done and can't contribute
  yourself, I can be hired.
