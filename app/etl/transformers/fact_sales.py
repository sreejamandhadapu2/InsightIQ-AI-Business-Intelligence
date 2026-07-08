"""
Fact Sales Transformer

Builds the FactSales table.
"""

from typing import Dict

import pandas as pd


class FactSalesTransformer:
    """
    Builds the FactSales table.
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:

        self.sales_header = tables["SalesOrderHeader"]
        self.sales_detail = tables["SalesOrderDetail"]

        self.dim_product = tables["DimProduct"]
        self.dim_customer = tables["DimCustomer"]
        self.dim_date = tables["DimDate"]
        self.dim_territory = tables["DimTerritory"]

    def build_fact(self) -> pd.DataFrame:

        merged = self._merge_sales()

        merged = self._join_dimensions(merged)

        fact = self._select_columns(merged)

        fact = self._generate_surrogate_keys(fact)

        return fact

    def _merge_sales(self) -> pd.DataFrame:

        merged = self.sales_detail.merge(
            self.sales_header,
            on="SalesOrderID",
            how="inner",
        )

        return merged

    def _join_dimensions(self, df: pd.DataFrame) -> pd.DataFrame:

        # Product
        df = df.merge(
            self.dim_product[
                [
                    "ProductID",
                    "ProductKey",
                ]
            ],
            on="ProductID",
            how="left",
        )

        # Customer
        df = df.merge(
            self.dim_customer[
                [
                    "CustomerID",
                    "CustomerKey",
                ]
            ],
            on="CustomerID",
            how="left",
        )

        # Date
        df["DateKey"] = (
            pd.to_datetime(df["OrderDate"])
            .dt.strftime("%Y%m%d")
            .astype(int)
        )

        df = df.merge(
            self.dim_date[
                [
                    "DateKey",
                ]
            ],
            on="DateKey",
            how="left",
        )

        # Territory
        df = df.merge(
            self.dim_territory[
                [
                    "TerritoryID",
                    "TerritoryKey",
                ]
            ],
            on="TerritoryID",
            how="left",
        )

        return df
    def _select_columns(self, df: pd.DataFrame) -> pd.DataFrame:

        fact = df[
            [
                "SalesOrderID",
                "SalesOrderDetailID",
                "ProductKey",
                "CustomerKey",
                "DateKey",
                "TerritoryKey",
                "OrderQty",
                "UnitPrice",
                "UnitPriceDiscount",
                "LineTotal",
            ]
        ].copy()

        return fact

    def _generate_surrogate_keys(self, df: pd.DataFrame) -> pd.DataFrame:

        df.insert(
            0,
            "SalesKey",
            range(1, len(df) + 1),
        )

        return df