"""
Territory Dimension Transformer

Builds the DimTerritory table from AdventureWorks.
"""

import pandas as pd


class TerritoryTransformer:
    """
    Builds the Territory Dimension (DimTerritory).
    """

    def __init__(self, territory: pd.DataFrame) -> None:
        self.territory = territory

    def build_dimension(self) -> pd.DataFrame:

        dim_territory = self.territory[
            [
                "TerritoryID",
                "Name",
                "CountryRegionCode",
                "Group",
            ]
        ].copy()

        dim_territory.rename(
            columns={
                "Name": "Region",
                "Group": "Continent",
            },
            inplace=True,
        )

        dim_territory.insert(
            0,
            "TerritoryKey",
            range(1, len(dim_territory) + 1),
        )

        dim_territory.fillna("Unknown", inplace=True)

        return dim_territory