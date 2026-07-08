from app.database.sql_server import SQLServerConnection
from app.etl.extractor import Extractor
from app.etl.transformers.territory import TerritoryTransformer


def main():

    db = SQLServerConnection()

    extractor = Extractor(db.get_engine())

    territory = extractor.extract_table("Sales.SalesTerritory")

    transformer = TerritoryTransformer(territory)

    dim_territory = transformer.build_dimension()

    print(dim_territory)

    print("\nColumns:")
    print(dim_territory.columns.tolist())

    print("\nShape:")
    print(dim_territory.shape)

    db.close()


if __name__ == "__main__":
    main()