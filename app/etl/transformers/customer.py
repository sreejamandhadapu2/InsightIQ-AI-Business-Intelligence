"""
Customer Dimension Transformer

Builds the DimCustomer table from AdventureWorks source tables.
"""

from typing import Dict

import pandas as pd


class CustomerTransformer:
    """
    Builds the Customer Dimension (DimCustomer).
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:
        """
        Initialize the transformer.
        """

        self.customer = tables["Customer"]
        self.person = tables["Person"]
        self.business_entity_address = tables["BusinessEntityAddress"]
        self.address = tables["Address"]
        self.state = tables["StateProvince"]
        self.country = tables["CountryRegion"]

    def build_dimension(self) -> pd.DataFrame:
        """
        Build the customer dimension.
        """

        merged_df = self._merge_tables()

        dim_customer = self._select_columns(merged_df)

        dim_customer = self._generate_surrogate_keys(dim_customer)

        return dim_customer

    def _merge_tables(self) -> pd.DataFrame:
        """
        Merge all customer-related tables.
        """

        # Keep only individual customers
        customer = self.customer[self.customer["PersonID"].notna()].copy()

        # Customer -> Person
        merged = customer.merge(
            self.person,
            left_on="PersonID",
            right_on="BusinessEntityID",
            how="left",
        )

        # Person -> BusinessEntityAddress
        merged = merged.merge(
            self.business_entity_address,
            on="BusinessEntityID",
            how="left",
        )

        # BusinessEntityAddress -> Address
        merged = merged.merge(
            self.address,
            on="AddressID",
            how="left",
        )

        # Address -> StateProvince
        merged = merged.merge(
            self.state,
            on="StateProvinceID",
            how="left",
            suffixes=("", "_State"),
        )

        # StateProvince -> CountryRegion
        merged = merged.merge(
            self.country,
            on="CountryRegionCode",
            how="left",
            suffixes=("", "_Country"),
        )

        return merged

    def _select_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select required warehouse columns.
        """

        dim_customer = pd.DataFrame()

        dim_customer["CustomerID"] = df["CustomerID"]

        dim_customer["CustomerName"] = (
            df["FirstName"].fillna("")
            + " "
            + df["LastName"].fillna("")
        ).str.strip()

        dim_customer["CustomerType"] = df["PersonType"]

        dim_customer["City"] = df["City"]

        # StateProvince.Name
        dim_customer["State"] = df["Name"]

        # CountryRegion.Name
        dim_customer["Country"] = df["Name_Country"]

        dim_customer.fillna("Unknown", inplace=True)

        return dim_customer

    def _generate_surrogate_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate CustomerKey.
        """

        df.insert(0, "CustomerKey", range(1, len(df) + 1))

        return df