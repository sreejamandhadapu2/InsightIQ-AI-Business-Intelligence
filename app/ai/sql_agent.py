"""
Gemini SQL Agent

Converts natural language questions into PostgreSQL SQL.
"""

import re

from google import genai

from app.config.settings import Settings
from app.prompts.sql_prompt import SYSTEM_PROMPT


class SQLAgent:
    """
    Generates PostgreSQL SQL using Gemini.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

    def _clean_sql(self, sql: str) -> str:
        """
        Clean Gemini response and return executable SQL.
        """

        # Remove markdown
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        # Remove optional explanation line
        sql = re.sub(
            r"^Here.*?:",
            "",
            sql,
            flags=re.IGNORECASE,
        )

        return sql.strip()

    def generate_sql(
        self,
        question: str,
    ) -> str:
        """
        Generate SQL from a natural language question.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                SYSTEM_PROMPT,
                question,
            ],
        )

        sql = response.text

        return self._clean_sql(sql)