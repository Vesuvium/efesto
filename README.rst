Efesto
======
|Pypi| |Build Status|

A micro REST API meant to be used almost out of the box with other
microservices.

It kickstarts you by providing a simple way to build a backend and expose it.
Efesto uses PostgreSQL and JWTs for authentication.

Efesto follows the UNIX principle of doing one thing and well, leaving you the
freedom of choice about other components (authentication, caching, rate-limiting,
load balancer).

Installing
---------------------
Install efesto, possibly in a virtual environment::

    pip install efesto

Create a postgresql database and export the database url::

    export db_url=postgres://postgres:postgres@localhost:5432/efesto

Export the jwt secret::

    export jwt_secret=secret

Populate the db::

    efesto quickstart

Create an admin::

    efesto create_user tofu --superuser

Now you can start efesto, with either uwsgi or gunicorn::

    gunicorn "efesto.App:App.run()"

Efesto should now be running, let's make sure it is. Create a jwt with the secret
you have configured. Efesto comes with an helper for that::

    efesto token tofu 1000

Send a request with the token::

     curl http://localhost:8000/users -H "Authorization: Bearer token"

Success! Efesto is running fine. Read the complete
`documentation <http://efesto.readthedocs.io>`_  to find out more

Performance
-----------
Efesto performs at about 200 requests/second on a small digital ocean
droplet, for requests that include JWT authentication, fetching data and
printing out JSON.

You have seen 100k requests benchmarks, but don't be fooled:
most benchmarks from authors are made so that their package comes to the top
and do not reflect real conditions.

That said, Efesto's did not reach its maximum and a lot can be done to improve
its performance.


Notes from the author
----------------------
- Efesto is not meant to be the solution to all problems. It can be quite good
  as a prototyping and early stage backend, less so on the long term (see below)

- Efesto lacks some strategic features and I can only put a limited amount
  of time into Efesto. If you want some features done and can't contribute
  yourself, I can be hired.


.. |Build Status| image:: https://img.shields.io/travis/getefesto/efesto.svg?maxAge=3600&style=for-the-badge
   :target: https://travis-ci.org/getefesto/efesto
.. |Pypi| image:: https://img.shields.io/pypi/v/efesto.svg?maxAge=3600&style=for-the-badge
   :target: https://pypi.python.org/pypi/efesto
.. |Docs| documentation :target: http://efesto.readthedocs.io
