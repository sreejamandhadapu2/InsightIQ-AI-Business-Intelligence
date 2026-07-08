from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor


def main():

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

    tables = extractor.extract_multiple_tables(
        [
            "Production.Product",
            "Production.ProductSubcategory",
            "Production.ProductCategory",
        ]
    )

    for name, df in tables.items():

        print(f"\n{name}")

        print(df.head())

        print(df.shape)

    db.close()


if __name__ == "__main__":
    main()