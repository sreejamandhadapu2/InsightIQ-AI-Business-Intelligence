"""
Executive Dashboard Service
"""

import pandas as pd

from app.database.postgres import PostgreSQLConnection
from app.analytics.dashboard_query_builder import DashboardQueryBuilder


class DashboardService:

    def __init__(self):

        self.db = PostgreSQLConnection()

        self.engine = self.db.get_engine()

    # =====================================================
    # Dashboard Filters
    # =====================================================

    def get_years(self):

        sql = """
        SELECT DISTINCT
            year
        FROM dim_date
        ORDER BY year
        """

        return (
            pd.read_sql(
                sql,
                self.engine,
            )["year"]
            .astype(str)
            .tolist()
        )

    def get_regions(self):

        sql = """
        SELECT DISTINCT
            region
        FROM dim_territory
        WHERE region IS NOT NULL
        ORDER BY region
        """

        return (
            pd.read_sql(
                sql,
                self.engine,
            )["region"]
            .tolist()
        )

    def get_categories(self):

        sql = """
        SELECT DISTINCT
            category
        FROM dim_product
        WHERE category IS NOT NULL
        ORDER BY category
        """

        return (
            pd.read_sql(
                sql,
                self.engine,
            )["category"]
            .tolist()
        )

    # =====================================================
    # KPI Cards
    # =====================================================

    def total_revenue(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            COALESCE(
                SUM(fs.line_total),
                0
            ) AS revenue

        FROM fact_sales fs

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0, 0]
    def total_orders(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            COUNT(
                DISTINCT fs.sales_order_id
            ) AS orders

        FROM fact_sales fs

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0, 0]


    def total_customers(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            COUNT(
                DISTINCT fs.customer_key
            ) AS customers

        FROM fact_sales fs

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0, 0]


    def total_products(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            COUNT(
                DISTINCT fs.product_key
            ) AS products

        FROM fact_sales fs

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0, 0]

    # =====================================================
    # Monthly Revenue
    # =====================================================
    def monthly_revenue(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            d.year,
            d.month,
            d.month_name,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}

        GROUP BY
            d.year,
            d.month,
            d.month_name

        ORDER BY
            d.year,
            d.month
        """

        df = pd.read_sql(
            sql,
            self.engine,
        )

        df["Period"] = (
            df["year"].astype(str)
            + "-"
            + df["month_name"].str[:3]
        )

        return df

    # =====================================================
    # Top Products
    # =====================================================

    def top_products(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dp.product_name,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        {filters}

        GROUP BY
            dp.product_name

        ORDER BY
            revenue DESC

        LIMIT 10
        """

        return pd.read_sql(
            sql,
            self.engine,
        )

    # =====================================================
    # Revenue by Territory
    # =====================================================
    def revenue_by_territory(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dt.region,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}

        GROUP BY
            dt.region

        ORDER BY
            revenue DESC
        """

        return pd.read_sql(
            sql,
            self.engine,
        )

    # =====================================================
    # Revenue by Category
    # =====================================================

    def revenue_by_category(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dp.category,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        {filters}

        GROUP BY
            dp.category

        ORDER BY
            revenue DESC
        """

        return pd.read_sql(
            sql,
            self.engine,
        )

    # =====================================================
    # Top Customers
    # =====================================================

    def top_customers(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dc.customer_name,
            COUNT(DISTINCT fs.sales_order_id) AS orders

        FROM fact_sales fs

        JOIN dim_customer dc
            ON fs.customer_key = dc.customer_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}

        GROUP BY
            dc.customer_name

        ORDER BY
            orders DESC

        LIMIT 10
        """

        return pd.read_sql(
            sql,
            self.engine,
        )

    # =====================================================
    # Top Regions
    # =====================================================

    def top_regions(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dt.region,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}

        GROUP BY
            dt.region

        ORDER BY
            revenue DESC

        LIMIT 10
        """

        return pd.read_sql(
            sql,
            self.engine,
        )

    # =====================================================
    # Executive Summary
    # =====================================================

    def best_product(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dp.product_name,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        {filters}

        GROUP BY
            dp.product_name

        ORDER BY
            revenue DESC

        LIMIT 1
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0]

    def best_category(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dp.category,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        {filters}

        GROUP BY
            dp.category

        ORDER BY
            revenue DESC

        LIMIT 1
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0]
    def best_region(
        self,
        year="All",
        region="All",
        category="All",
    ):

        filters = DashboardQueryBuilder.build_where_clause(
            year,
            region,
            category,
        )

        sql = f"""
        SELECT
            dt.region,
            SUM(fs.line_total) AS revenue

        FROM fact_sales fs

        JOIN dim_territory dt
            ON fs.territory_key = dt.territory_key

        JOIN dim_date d
            ON fs.date_key = d.date_key

        JOIN dim_product dp
            ON fs.product_key = dp.product_key

        {filters}

        GROUP BY
            dt.region

        ORDER BY
            revenue DESC

        LIMIT 1
        """

        return pd.read_sql(
            sql,
            self.engine,
        ).iloc[0]

    def executive_recommendation(
        self,
        year="All",
        region="All",
        category="All",
    ):

        try:

            best_product = self.best_product(
                year,
                region,
                category,
            )

            best_category = self.best_category(
                year,
                region,
                category,
            )

            best_region = self.best_region(
                year,
                region,
                category,
            )

            return (
                f"'{best_category['category']}' is the highest-performing "
                f"category, led by '{best_product['product_name']}'. "
                f"The '{best_region['region']}' region generated the highest revenue. "
                f"Consider increasing inventory, promotions, and customer engagement "
                f"for this category while expanding successful regional strategies."
            )

        except Exception:

            return (
                "No recommendation is available because the selected filters "
                "did not return any sales data."
            )

    # =====================================================
    # Close Connection
    # =====================================================

    def close(self):

        self.db.close()