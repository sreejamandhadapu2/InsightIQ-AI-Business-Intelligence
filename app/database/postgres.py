from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import Settings


class PostgreSQLConnection:

    def __init__(self):

        connection_string = (
            f"postgresql+psycopg2://"
            f"{Settings.POSTGRES_USER}:"
            f"{Settings.POSTGRES_PASSWORD}@"
            f"{Settings.POSTGRES_HOST}:"
            f"{Settings.POSTGRES_PORT}/"
            f"{Settings.POSTGRES_DATABASE}"
        )

        self._engine = create_engine(connection_string)

    def get_engine(self) -> Engine:
        return self._engine

    def test_connection(self):

        try:

            with self._engine.connect():
                print("✅ Successfully connected to PostgreSQL!")

            return True

        except Exception as e:

            print(e)

            return False

    def close(self):

        self._engine.dispose()