# Middlewares

Efesto uses a number of middlewares to make it possible to customize is
behaviour.


## Authentication

Rejects requests without a JWT that matches the secret and audience, unless an
endpoint is public.

Authenticated requests should have an authorization header set to
`Bearer <JWT>`.

The JWT should be generated with the configured secret and audience, and have
the corresponding user identified set as `sub` claim:

```json
{"aud": "<your-audience>", "sub": "<user-identifier>", "exp": "<future-timestamp>"}
```

## Clacks

Adds an `X-Clacks-Overhead` header set to `GNU Terry Pratchett` to responses.

## Db

Responsible for database connections. Supports sqlite or postgres.

## Json

Encodes responses' body to Json

## Log

Logs processed responses

## Msgpack

Encodes responses' body to MsgPack
