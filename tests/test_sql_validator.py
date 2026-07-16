from app.ai.sql_validator import SQLValidator


def main():

    sql = """
    SELECT *
    FROM dim_product
    LIMIT 5;
    """

    if SQLValidator.validate(sql):

        print("✅ SQL is valid")


if __name__ == "__main__":
    main()