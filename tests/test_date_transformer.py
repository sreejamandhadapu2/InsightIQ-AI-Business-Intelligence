from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.date_dimension import DateTransformer


def main():

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

    sales_header = extractor.extract_columns(
        "Sales.SalesOrderHeader",
        [
            "OrderDate",
            "DueDate",
            "ShipDate",
        ],
    )

    transformer = DateTransformer(sales_header)

    dim_date = transformer.build_dimension()

    print(dim_date.head())

    print("\nColumns:")
    print(dim_date.columns.tolist())

    print("\nShape:")
    print(dim_date.shape)

    db.close()


if __name__ == "__main__":
    main()