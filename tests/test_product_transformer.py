from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.product import ProductTransformer


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

    transformer = ProductTransformer(tables)

    dim_product = transformer.build_dimension()

    print(dim_product.head())

    print("\nColumns:")
    print(dim_product.columns.tolist())

    print("\nShape:")
    print(dim_product.shape)
    print(dim_product["Category"].value_counts(dropna=False))
    print(dim_product["Subcategory"].value_counts(dropna=False))

    db.close()


if __name__ == "__main__":
    main()