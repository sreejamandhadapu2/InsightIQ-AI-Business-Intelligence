"""
Data Loader

Loads transformed DataFrames into PostgreSQL.
"""

import re
from typing import Dict

import pandas as pd
from sqlalchemy.engine import Engine


class Loader:
    """
    Load DataFrames into PostgreSQL.
    """

    def __init__(self, engine: Engine) -> None:

        self.engine = engine

    @staticmethod
    def _to_snake_case(column: str) -> str:
        """
        Convert CamelCase/PascalCase to snake_case.

        Examples:
            ProductKey -> product_key
            CustomerID -> customer_id
            SalesOrderID -> sales_order_id
            SalesOrderDetailID -> sales_order_detail_id
            BusinessEntityID -> business_entity_id
        """

        # Split acronym followed by normal word
        column = re.sub(
            r"([A-Z]+)([A-Z][a-z])",
            r"\1_\2",
            column,
        )

        # Split lowercase/digit followed by uppercase
        column = re.sub(
            r"([a-z0-9])([A-Z])",
            r"\1_\2",
            column,
        )

        return column.lower()

    def _prepare_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare dataframe before loading.
        """

        dataframe = dataframe.copy()

        dataframe.columns = [
            self._to_snake_case(column)
            for column in dataframe.columns
        ]

        return dataframe

    def load_table(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace",
    ) -> None:
        """
        Load a single DataFrame into PostgreSQL.
        """

        dataframe = self._prepare_dataframe(dataframe)

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