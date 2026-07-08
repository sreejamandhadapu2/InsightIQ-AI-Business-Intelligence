"""
Gemini SQL Agent

Converts natural language into PostgreSQL SQL.
"""

from google import genai

from app.config.settings import Settings
from app.prompts.sql_prompt import SYSTEM_PROMPT


class SQLAgent:
    """
    Generates SQL queries using Gemini.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

    def generate_sql(
        self,
        question: str,
    ) -> str:
        """
        Generate PostgreSQL SQL from a natural language question.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                SYSTEM_PROMPT,
                question,
            ],
        )

        return response.text.strip()