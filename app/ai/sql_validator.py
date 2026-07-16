"""
SQL Validator

Validates AI-generated SQL before execution.
"""

import re


class SQLValidator:
    """
    Validates SQL queries for safety.
    """

    ALLOWED_TABLES = {
        "dim_product",
        "dim_customer",
        "dim_date",
        "dim_territory",
        "fact_sales",
    }

    FORBIDDEN_KEYWORDS = {
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    }

    @classmethod
    def validate(cls, sql: str) -> bool:
        """
        Validate SQL query.
        """

        sql_upper = sql.upper()

        # Only SELECT queries
        if not sql_upper.strip().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed.")

        # Reject multiple statements
        if sql.count(";") > 1:
            raise ValueError("Multiple SQL statements are not allowed.")

        # Reject dangerous keywords
        for keyword in cls.FORBIDDEN_KEYWORDS:

            if keyword in sql_upper:

                raise ValueError(
                    f"Forbidden SQL keyword detected: {keyword}"
                )

        # Check table names
        tables = re.findall(
            r"(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            sql,
            flags=re.IGNORECASE,
        )

        for table in tables:

            if table.lower() not in cls.ALLOWED_TABLES:

                raise ValueError(
                    f"Unauthorized table: {table}"
                )

        return True