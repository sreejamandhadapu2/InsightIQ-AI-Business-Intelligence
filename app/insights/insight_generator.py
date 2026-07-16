"""
AI Business Insight Generator
"""

from google import genai

from app.config.settings import Settings


class InsightGenerator:
    """
    Generates executive business insights using Gemini.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

    def generate_insight(
        self,
        question,
        dataframe,
    ):

        if dataframe.empty:

            return (
                "No data available for analysis."
            )

        preview = dataframe.head(20).to_markdown(
            index=False
        )

        prompt = f"""
You are a Senior Business Intelligence Analyst.

A business user asked:

{question}

The query returned:

{preview}

Generate a concise executive summary.

Rules:

- Maximum 5 bullet points.
- Highlight important business trends.
- Mention highest and lowest values if applicable.
- Mention anomalies or outliers if present.
- Give ONE actionable business recommendation.
- Never mention SQL, tables, databases or technical details.
- Keep the language simple and professional.
- If the query is about Top Customers, Top Products, Top Categories or Revenue, explain what the business can learn from it.
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            if (
                response
                and hasattr(response, "text")
                and response.text
            ):

                return response.text.strip()

            return (
                "AI could not generate business insights."
            )

        except Exception as error:

            error_message = str(error)

            if "RESOURCE_EXHAUSTED" in error_message:

                return (
                    "⚠ Gemini API quota exceeded. "
                    "Please try again later."
                )

            if "API_KEY" in error_message.upper():

                return (
                    "⚠ Invalid Gemini API Key."
                )

            return (
                "⚠ Unable to generate AI Business Insights."
            )