"""
Test SQL Server Connection
"""

from app.database.sql_server import SQLServerConnection


def main() -> None:
    """Test SQL Server database connection."""

    db = SQLServerConnection()

    if db.test_connection():
        print("✅ Successfully connected to SQL Server!")
    else:
        print("❌ Failed to connect to SQL Server.")

    db.close()


if __name__ == "__main__":
    main()