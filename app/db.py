import os
import mysql.connector

# Single-database config. Override any of these with environment variables
# in production instead of editing this file directly.
DB_CONFIG = {
    "host": os.environ.get("CALLHUB_DB_HOST", "localhost"),
    "user": os.environ.get("CALLHUB_DB_USER", "root"),
    "password": os.environ.get("CALLHUB_DB_PASSWORD", ""),
    "database": os.environ.get("CALLHUB_DB_NAME", "CallHub"),
}


def get_connection():
    """Return a fresh MySQL connection using DB_CONFIG.

    Every route opens a connection, uses it, then closes it (see routes/*.py).
    That's fine at this project's scale; if this ever needs to handle real
    concurrent traffic, switch this to a pooled connection
    (mysql.connector.pooling.MySQLConnectionPool) instead of opening a new
    TCP connection per request.
    """
    return mysql.connector.connect(**DB_CONFIG)
