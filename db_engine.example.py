"""
Example database engine configuration.
Copy this file to db_engine.py and update with your actual credentials.
"""
import oracledb
from sqlalchemy import create_engine

# Oracle database configuration
DSN_HOST = 'your-db-host'
DSN_PORT = '1521'
DSN_SERVICE_NAME = 'your-service-name'

DB_USER = 'your-username'
DB_PASSWORD = 'your-password'

# Create DSN
dsn = oracledb.makedsn(
    DSN_HOST, DSN_PORT, service_name=DSN_SERVICE_NAME
)

# Create connection pool
pool = oracledb.SessionPool(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=dsn,
    min=2,
    max=5,
    increment=1,
    encoding="UTF-8"
)

# Acquire connection
conn = pool.acquire()
db = conn.cursor()

# Create SQLAlchemy engine
engine = create_engine(
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DSN_HOST}:{DSN_PORT}/?service_name={DSN_SERVICE_NAME}"
)
