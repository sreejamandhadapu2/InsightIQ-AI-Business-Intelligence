from app.database.postgres import PostgreSQLConnection


def main():

    db = PostgreSQLConnection()

    db.test_connection()

    db.close()


if __name__ == "__main__":
    main()