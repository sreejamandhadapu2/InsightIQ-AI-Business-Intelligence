"""
Build All Dimension Tables

This script builds all warehouse dimensions and saves them
to the data/processed folder.
"""

from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.product import ProductTransformer
from app.etl.transformers.customer import CustomerTransformer
from app.etl.transformers.date_dimension import DateTransformer
from app.etl.transformers.territory import TerritoryTransformer
from app.utils.file_manager import FileManager


def main():

    print("=" * 60)
    print("Building Warehouse Dimensions")
    print("=" * 60)

    db = SQLServerConnection()
    extractor = Extractor(db.get_engine())
    file_manager = FileManager()

    # -------------------------------------------------
    # DimProduct
    # -------------------------------------------------

    print("\nBuilding DimProduct...")

    product_tables = extractor.extract_multiple_tables(
        [
            "Production.Product",
            "Production.ProductSubcategory",
            "Production.ProductCategory",
        ]
    )

    dim_product = ProductTransformer(product_tables).build_dimension()

    file_manager.save_dataframe(
        dim_product,
        "dim_product.csv",
    )

    # -------------------------------------------------
    # DimCustomer
    # -------------------------------------------------

    print("\nBuilding DimCustomer...")

    customer = extractor.extract_table("Sales.Customer")

    person = extractor.extract_table("Person.Person")

    business_entity_address = extractor.extract_table(
        "Person.BusinessEntityAddress"
    )

    address = extractor.extract_columns(
        "Person.Address",
        [
            "AddressID",
            "City",
            "StateProvinceID",
        ],
    )

    state = extractor.extract_table(
        "Person.StateProvince"
    )

    country = extractor.extract_table(
        "Person.CountryRegion"
    )

    customer_tables = {
        "Customer": customer,
        "Person": person,
        "BusinessEntityAddress": business_entity_address,
        "Address": address,
        "StateProvince": state,
        "CountryRegion": country,
    }

    dim_customer = CustomerTransformer(
        customer_tables
    ).build_dimension()

    file_manager.save_dataframe(
        dim_customer,
        "dim_customer.csv",
    )

    # -------------------------------------------------
    # DimDate
    # -------------------------------------------------

    print("\nBuilding DimDate...")

    sales_header = extractor.extract_columns(
        "Sales.SalesOrderHeader",
        [
            "OrderDate",
            "DueDate",
            "ShipDate",
        ],
    )

    dim_date = DateTransformer(
        sales_header
    ).build_dimension()

    file_manager.save_dataframe(
        dim_date,
        "dim_date.csv",
    )

    # -------------------------------------------------
    # DimTerritory
    # -------------------------------------------------

    print("\nBuilding DimTerritory...")

    territory = extractor.extract_table(
        "Sales.SalesTerritory"
    )

    dim_territory = TerritoryTransformer(
        territory
    ).build_dimension()

    file_manager.save_dataframe(
        dim_territory,
        "dim_territory.csv",
    )

    db.close()

    print("\n" + "=" * 60)
    print("🎉 All dimensions built successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()