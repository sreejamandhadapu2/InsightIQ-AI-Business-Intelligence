"""
Build FactSales Table

This script builds the FactSales table and saves it
to data/processed/fact_sales.csv.
"""

from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.fact_sales import FactSalesTransformer
from app.utils.file_manager import FileManager


def main():

    print("=" * 60)
    print("Building FactSales")
    print("=" * 60)

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

    fm = FileManager()

    # Source tables
    sales_header = extractor.extract_table("Sales.SalesOrderHeader")

    sales_detail = extractor.extract_table("Sales.SalesOrderDetail")

    # Load dimensions
    dim_product = fm.load_dataframe("dim_product.csv")

    dim_customer = fm.load_dataframe("dim_customer.csv")

    dim_date = fm.load_dataframe("dim_date.csv")

    dim_territory = fm.load_dataframe("dim_territory.csv")

    tables = {
        "SalesOrderHeader": sales_header,
        "SalesOrderDetail": sales_detail,
        "DimProduct": dim_product,
        "DimCustomer": dim_customer,
        "DimDate": dim_date,
        "DimTerritory": dim_territory,
    }

    transformer = FactSalesTransformer(tables)

    fact_sales = transformer.build_fact()

    fm.save_dataframe(
        fact_sales,
        "fact_sales.csv",
    )

    db.close()

    print("\nFactSales Built Successfully!")


if __name__ == "__main__":
    main()