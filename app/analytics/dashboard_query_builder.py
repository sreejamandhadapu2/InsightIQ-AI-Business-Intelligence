"""
Dashboard Query Builder
"""


class DashboardQueryBuilder:

    @staticmethod
    def build_where_clause(
        year="All",
        region="All",
        category="All",
    ):

        conditions = []

        if year != "All":
            conditions.append(
                f"d.year = {year}"
            )

        if region != "All":
            conditions.append(
                f"dt.region = '{region}'"
            )

        if category != "All":
            conditions.append(
                f"dp.category = '{category}'"
            )

        if not conditions:
            return ""

        return (
            "WHERE "
            + " AND ".join(
                conditions
            )
        )