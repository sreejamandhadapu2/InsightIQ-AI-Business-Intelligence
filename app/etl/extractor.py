"""
Data Extraction Module

Provides reusable methods to extract data from SQL Server.
"""

from typing import Dict, List

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


class Extractor:
    """
    Extract data from SQL Server.
    """

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def extract_table(self, table_name: str) -> pd.DataFrame:
        """
        Extract an entire table.
        """

        query = f"SELECT * FROM {table_name}"

        return pd.read_sql(query, self.engine)

    def extract_query(self, query: str) -> pd.DataFrame:
        """
        Execute a custom SQL query.
        """

        return pd.read_sql(text(query), self.engine)

    def extract_columns(
        self,
        table_name: str,
        columns: List[str]
    ) -> pd.DataFrame:
        """
        Extract only required columns from a table.
        """

        cols = ", ".join(columns)

        query = f"""
        SELECT {cols}
        FROM {table_name}
        """

        return pd.read_sql(query, self.engine)

    def extract_multiple_tables(
        self,
        table_names: List[str]
    ) -> Dict[str, pd.DataFrame]:

        tables = {}

        for table in table_names:

            table_key = table.split(".")[-1]

            tables[table_key] = self.extract_table(table)

        return tables