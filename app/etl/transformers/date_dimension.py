"""
Date Dimension Transformer

Builds the DimDate table from AdventureWorks sales dates.
"""

import pandas as pd


class DateTransformer:
    """
    Builds the Date Dimension (DimDate).
    """

    def __init__(self, sales_header: pd.DataFrame) -> None:

        self.sales_header = sales_header

    def build_dimension(self) -> pd.DataFrame:

        dates = pd.concat(
            [
                self.sales_header["OrderDate"],
                self.sales_header["DueDate"],
                self.sales_header["ShipDate"],
            ]
        )

        dates = pd.to_datetime(dates)

        dates = dates.dropna().drop_duplicates().sort_values()

        dim_date = pd.DataFrame()

        dim_date["FullDate"] = dates

        dim_date["DateKey"] = dim_date["FullDate"].dt.strftime("%Y%m%d").astype(int)

        dim_date["Day"] = dim_date["FullDate"].dt.day

        dim_date["Month"] = dim_date["FullDate"].dt.month

        dim_date["MonthName"] = dim_date["FullDate"].dt.month_name()

        dim_date["Quarter"] = "Q" + dim_date["FullDate"].dt.quarter.astype(str)

        dim_date["Year"] = dim_date["FullDate"].dt.year

        dim_date["Week"] = dim_date["FullDate"].dt.isocalendar().week.astype(int)

        dim_date["DayOfWeek"] = dim_date["FullDate"].dt.day_name()

        dim_date["IsWeekend"] = dim_date["FullDate"].dt.dayofweek >= 5

        dim_date.insert(0, "DateKey", dim_date.pop("DateKey"))

        return dim_date