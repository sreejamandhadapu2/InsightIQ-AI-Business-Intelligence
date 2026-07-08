"""
Query Service

Executes SQL queries against the PostgreSQL data warehouse.
"""

import pandas as pd

from app.database.postgres import PostgreSQLConnection


class QueryService:
    """
    Executes SQL queries and returns results.
    """

    def __init__(self) -> None:

        self.database = PostgreSQLConnection()

        self.engine = self.database.get_engine()

    def execute_query(
        self,
        sql: str,
    ) -> pd.DataFrame:
        """
        Execute a SQL query and return a DataFrame.
        """

        try:

            dataframe = pd.read_sql(
                sql,
                self.engine,
            )

            return dataframe

        except Exception as error:

            raise RuntimeError(
                f"Query execution failed:\n{error}"
            ) from error

    def close(self) -> None:
        """
        Close database connection.
        """

        self.database.close()