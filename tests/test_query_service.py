from app.services.query_service import QueryService


def main():

    service = QueryService()

    sql = """
    SELECT *
    FROM dim_product
    LIMIT 5;
    """

    dataframe = service.execute_query(sql)

    print(dataframe)

    print("\nShape:")
    print(dataframe.shape)

    service.close()


if __name__ == "__main__":
    main()