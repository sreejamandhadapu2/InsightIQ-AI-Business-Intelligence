from app.ai.sql_agent import SQLAgent


def main():

    agent = SQLAgent()

    sql = agent.generate_sql(
        "Show me the top 5 selling products by revenue."
    )

    print(sql)


if __name__ == "__main__":
    main()