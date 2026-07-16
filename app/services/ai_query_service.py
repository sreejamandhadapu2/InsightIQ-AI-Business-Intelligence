"""
AI Query Service

Coordinates the AI SQL pipeline.
"""

import pandas as pd

from app.ai.sql_agent import SQLAgent
from app.ai.sql_validator import SQLValidator
from app.services.query_service import QueryService


class AIQueryService:
    """
    End-to-end AI SQL Service.
    """

    def __init__(self):

        self.agent = SQLAgent()

        self.query_service = QueryService()

    def ask(
        self,
        question: str,
    ) -> tuple[str, pd.DataFrame]:

        # Step 1
        sql = self.agent.generate_sql(question)

        # Step 2
        SQLValidator.validate(sql)

        # Step 3
        dataframe = self.query_service.execute_query(sql)

        return sql, dataframe

    def close(self):

        self.query_service.close()