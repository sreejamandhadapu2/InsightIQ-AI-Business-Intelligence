from app.config.tables import TABLES
from app.database.postgres import PostgreSQLConnection
from app.etl.loader import Loader
from app.utils.file_manager import FileManager


def main():

    print("=" * 60)
    print("Loading Warehouse into PostgreSQL")
    print("=" * 60)

    postgres = PostgreSQLConnection()

    loader = Loader(postgres.get_engine())

    file_manager = FileManager()

    tables = {}

    for table_name, csv_file in TABLES.items():

        print(f"Loading {csv_file}...")

        tables[table_name] = file_manager.load_dataframe(csv_file)

    loader.load_multiple_tables(tables)

    postgres.close()

    print("\n" + "=" * 60)
    print("Warehouse Loaded Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()