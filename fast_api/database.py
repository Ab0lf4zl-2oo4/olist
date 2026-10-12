from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

SERVER = "DESKTOP-JKUS70M"
DATABASE = "ecommerce_dw"

connection_url = URL.create(
    "mssql+pyodbc",
    host=SERVER,
    database=DATABASE,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DB_NAME()")
        )
        return result.scalar()