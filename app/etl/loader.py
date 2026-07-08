"""
Data Loader

Loads transformed DataFrames into PostgreSQL.
"""

from typing import Dict

import pandas as pd
from sqlalchemy.engine import Engine


class Loader:
    """
    Load DataFrames into PostgreSQL.
    """

    def __init__(self, engine: Engine) -> None:
        """
        Initialize the loader.

        Parameters
        ----------
        engine : Engine
            SQLAlchemy PostgreSQL engine.
        """
        self.engine = engine

    def load_table(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace",
    ) -> None:
        """
        Load a single DataFrame into PostgreSQL.
        """

        dataframe.to_sql(
            name=table_name,
            con=self.engine,
            if_exists=if_exists,
            index=False,
        )

        print(f"✅ Loaded table: {table_name}")

    def load_multiple_tables(
        self,
        tables: Dict[str, pd.DataFrame],
        if_exists: str = "replace",
    ) -> None:
        """
        Load multiple DataFrames into PostgreSQL.
        """

        for table_name, dataframe in tables.items():

            self.load_table(
                dataframe,
                table_name,
                if_exists,
            )

        print("\n🎉 All tables loaded successfully!")