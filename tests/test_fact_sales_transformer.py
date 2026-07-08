from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.fact_sales import FactSalesTransformer


def main():

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

    sales_header = extractor.extract_table("Sales.SalesOrderHeader")

    sales_detail = extractor.extract_table("Sales.SalesOrderDetail")

    tables = {
    "SalesOrderHeader": sales_header,
    "SalesOrderDetail": sales_detail,
    "DimProduct": dim_product,
    "DimCustomer": dim_customer,
    "DimDate": dim_date,
    "DimTerritory": dim_territory,
}

    transformer = FactSalesTransformer(tables)

    merged = transformer.build_fact()

    print(merged.head())

    print("\nColumns:")
    print(merged.columns.tolist())

    print("\nShape:")
    print(merged.shape)

    db.close()


if __name__ == "__main__":
    main()