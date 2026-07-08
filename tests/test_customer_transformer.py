from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.customer import CustomerTransformer


def main():

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

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

    state = extractor.extract_table("Person.StateProvince")

    country = extractor.extract_table("Person.CountryRegion")

    tables = {
        "Customer": customer,
        "Person": person,
        "BusinessEntityAddress": business_entity_address,
        "Address": address,
        "StateProvince": state,
        "CountryRegion": country,
    }

    transformer = CustomerTransformer(tables)

    dim_customer = transformer.build_dimension()

    print(dim_customer.head())

    print("\nColumns:")
    print(dim_customer.columns.tolist())

    print("\nShape:")
    print(dim_customer.shape)

    db.close()


if __name__ == "__main__":
    main()