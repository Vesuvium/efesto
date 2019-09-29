# Command line

```
efesto install
```

Inits the configured database by creating the tables for users, fields and
types.


```
efesto create user <name> --superuser
```

Creates an user with the given name. If `--superuser` is passed, the user will
be a superuser.

```
efesto load <blueprint>
```

Loads a blueprint, creating the specified types and fields and the corresponding
tables.

```
efesto token <username> <expiration-in-days>
```

Creates a token for the given user that expires in the given days. Uses
the configured JWT_TOKEN and JWT_AUDIENCE

```
efesto version
```

Prints efesto's version.
