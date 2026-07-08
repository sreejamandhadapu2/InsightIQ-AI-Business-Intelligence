"""
SQL Server Database Connection

Provides a reusable SQL Server connection using SQLAlchemy.
"""

from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config.settings import Settings


class SQLServerConnection:
    """Manages SQL Server database connections."""

    def __init__(self) -> None:
        self._engine: Engine | None = None

    def create_engine(self) -> Engine:
        """Create and return a SQLAlchemy engine."""

        if self._engine is None:

            connection_string = (
                "mssql+pyodbc://@"
                f"{Settings.SQL_SERVER}/"
                f"{Settings.SQL_DATABASE}"
                f"?driver={quote_plus(Settings.SQL_DRIVER)}"
                "&trusted_connection=yes"
            )

            self._engine = create_engine(connection_string)

        return self._engine

    def get_engine(self) -> Engine:
        """Return the SQLAlchemy engine."""

        return self.create_engine()

    def test_connection(self) -> bool:
        """Test the database connection."""

        try:
            engine = self.get_engine()

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return True

        except Exception as error:
            print(f"Connection failed: {error}")
            return False

    def close(self) -> None:
        """Dispose the SQLAlchemy engine."""

        if self._engine:
            self._engine.dispose()