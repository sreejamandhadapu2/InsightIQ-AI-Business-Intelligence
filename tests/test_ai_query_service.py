from app.services.ai_query_service import AIQueryService


def main():

    service = AIQueryService()

    question = "Show me the top 5 products by revenue."

    sql, result = service.ask(question)

    print("\nGenerated SQL\n")
    print(sql)

    print("\nResults\n")
    print(result)

    service.close()


if __name__ == "__main__":
    main()