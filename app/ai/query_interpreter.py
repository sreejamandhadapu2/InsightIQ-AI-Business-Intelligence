"""
AI Query Interpreter
"""


class QueryInterpreter:

    @staticmethod
    def interpret(question):

        question = question.lower()

        interpretation = {
            "intent": "General Analysis",
            "metric": "Unknown",
            "filters": [],
            "visualization": "Bar Chart",
            "confidence": 50,
        }

        # ===============================
        # Intent
        # ===============================

        if "product" in question:
            interpretation["intent"] = "Product Analysis"

        elif "customer" in question:
            interpretation["intent"] = "Customer Analysis"

        elif "territory" in question or "region" in question:
            interpretation["intent"] = "Regional Analysis"

        elif "category" in question:
            interpretation["intent"] = "Category Analysis"

        elif "trend" in question or "month" in question:
            interpretation["intent"] = "Trend Analysis"

        # ===============================
        # Metric
        # ===============================

        if "revenue" in question:

            interpretation["metric"] = "Revenue"

        elif "orders" in question:

            interpretation["metric"] = "Orders"

        elif "sales" in question:

            interpretation["metric"] = "Sales"

        # ===============================
        # Filters
        # ===============================

        for year in [
            "2011",
            "2012",
            "2013",
            "2014",
        ]:

            if year in question:

                interpretation["filters"].append(
                    f"Year = {year}"
                )

        if "top 10" in question:

            interpretation["filters"].append(
                "Top 10"
            )

        # ===============================
        # Visualization
        # ===============================

        if "category" in question:

            interpretation["visualization"] = (
                "Pie Chart"
            )

        elif (
            "trend" in question
            or "month" in question
        ):

            interpretation["visualization"] = (
                "Line Chart"
            )

        elif (
            "top" in question
            or "highest" in question
        ):

            interpretation["visualization"] = (
                "Horizontal Bar Chart"
            )
        # ===============================
# Confidence Score
# ===============================

        confidence = 50

        if interpretation["intent"] != "General Analysis":
            confidence += 15

        if interpretation["metric"] != "Unknown":
            confidence += 15

        confidence += len(
            interpretation["filters"]
        ) * 10

        if interpretation["visualization"] != "Bar Chart":
            confidence += 10

        interpretation["confidence"] = min(
            confidence,
            100,
        )

        return interpretation