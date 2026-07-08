"""
Product Dimension Transformer

Builds the DimProduct table from AdventureWorks source tables.
"""

from typing import Dict

import pandas as pd


class ProductTransformer:
    """
    Builds the Product Dimension (DimProduct).
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:
        """
        Initialize the transformer.

        Parameters
        ----------
        tables : Dict[str, pd.DataFrame]
            Dictionary containing extracted AdventureWorks tables.
        """

        self.product = tables["Product"]
        self.subcategory = tables["ProductSubcategory"]
        self.category = tables["ProductCategory"]

    def build_dimension(self) -> pd.DataFrame:
        """
        Build the Product Dimension.

        Returns
        -------
        pd.DataFrame
            Product Dimension.
        """

        merged_df = self._merge_tables()

        dim_product = self._select_columns(merged_df)

        dim_product = self._generate_surrogate_keys(dim_product)

        return dim_product

    def _merge_tables(self) -> pd.DataFrame:
        """
        Merge Product, ProductSubcategory and ProductCategory tables.

        Returns
        -------
        pd.DataFrame
            Merged DataFrame.
        """

        # Product + ProductSubcategory
        merged_df = self.product.merge(
            self.subcategory,
            how="left",
            on="ProductSubcategoryID",
            suffixes=("", "_Subcategory")
        )

        # Merge with ProductCategory
        merged_df = merged_df.merge(
            self.category,
            how="left",
            on="ProductCategoryID",
            suffixes=("", "_Category")
        )

        return merged_df

    def _select_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select and rename warehouse columns.

        Parameters
        ----------
        df : pd.DataFrame
            Merged DataFrame.

        Returns
        -------
        pd.DataFrame
            Product Dimension columns.
        """

        dim_product = df[
            [
                "ProductID",
                "Name",
                "Name_Category",
                "Name_Subcategory",
                "Color",
                "StandardCost",
                "ListPrice",
            ]
        ].copy()

        dim_product.rename(
            columns={
                "Name": "ProductName",
                "Name_Category": "Category",
                "Name_Subcategory": "Subcategory",
            },
            inplace=True,
        )

        return dim_product

    def _generate_surrogate_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate ProductKey.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """

        df.insert(0, "ProductKey", range(1, len(df) + 1))

        return df