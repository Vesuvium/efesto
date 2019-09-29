# Configuration

Efesto is configured through environment variables.


# DB_URL

The database url. Defaults to `sqlite:///efesto.db`.

# DB_CONNECTIONS

The size of the database connections' pool. Defaults to `32`.

# DB_TIMEOUT

The timeout for pooled database connections. Defaults to `300` seconds.

# JWT_SECRET

The secret used for JWT. Defaults to `secret`.

# JWT_AUDIENCE

The audience of JWTs. Defaults to `efesto`.

# JWT_LEEWAY

Leeway for JWTs time-based claims (exp, iat, etc.). Defaults to `5` seconds.

# LOG_LEVEL

Efesto's log level. Efesto uses [loguru](https://github.com/Delgan/loguru) for
logging.

# LOG_FORMAT

Format for logs. Defaults to `[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}`

# MIDDLEWARES

The middlewares to use. Defaults to `db:authentication:json:log`.

Efesto does not verify that the middlewares pipeline is correct. It should
follow
`<db_middleware>:<authentication>:<mime encoder>:<extras>:<log_middleware>`

# PUBLIC_ENDPOINTS

Endpoints that do not require authentication. Defaults to `index,version`.
