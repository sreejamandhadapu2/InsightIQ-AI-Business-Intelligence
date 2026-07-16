"""
Smart Chart Generator
"""

import plotly.express as px
import streamlit as st


class ChartGenerator:

    @staticmethod
    def show_chart(dataframe, question=""):

        if dataframe.empty:
            return

        question = question.lower()

        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        text_columns = dataframe.select_dtypes(
            exclude="number"
        ).columns.tolist()

        # ============================================
        # Plain Detail Queries (No Chart)
        # ============================================

        if (
            (
                "details" in question
                or "list" in question
            )
            and "top" not in question
            and "highest" not in question
            and "lowest" not in question
            and "most" not in question
            and "least" not in question
        ):
            return

        # ============================================
        # Time Series
        # ============================================

        if (
            "month" in question
            or "monthly" in question
            or "year" in question
            or "trend" in question
            or "daily" in question
        ):

            if len(text_columns) >= 1 and len(numeric_columns) >= 1:

                fig = px.line(
                    dataframe,
                    x=text_columns[0],
                    y=numeric_columns[0],
                    markers=True,
                    title="Trend Analysis",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                return

        # ============================================
        # Category Distribution
        # ============================================

        if (
            "category" in question
            or "categories" in question
        ):

            if len(text_columns) >= 1 and len(numeric_columns) >= 1:

                fig = px.pie(
                    dataframe,
                    names=text_columns[0],
                    values=numeric_columns[0],
                    hole=0.45,
                    title="Category Distribution",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                return

        # ============================================
        # Territory / Region
        # ============================================

        if (
            "territory" in question
            or "region" in question
            or "country" in question
            or "continent" in question
        ):

            if len(text_columns) >= 1 and len(numeric_columns) >= 1:

                fig = px.bar(
                    dataframe,
                    x=text_columns[0],
                    y=numeric_columns[0],
                    title="Revenue by Region",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                return

        # ============================================
        # Ranking Queries
        # ============================================

        if (
            "top" in question
            or "highest" in question
            or "lowest" in question
            or "most" in question
            or "least" in question
            or "best" in question
            or "product" in question
            or "customer" in question
            or "employee" in question
            or "seller" in question
            or "orders" in question
        ):

            if len(text_columns) >= 1 and len(numeric_columns) >= 1:

                fig = px.bar(
                    dataframe,
                    x=numeric_columns[0],
                    y=text_columns[0],
                    orientation="h",
                    title="Ranking Analysis",
                )

                fig.update_layout(
                    yaxis=dict(autorange="reversed")
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                return

        # ============================================
        # Scatter Plot
        # ============================================

        if len(numeric_columns) >= 2:

            fig = px.scatter(
                dataframe,
                x=numeric_columns[0],
                y=numeric_columns[1],
                title="Relationship Analysis",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            return

        # ============================================
        # Default Bar Chart
        # ============================================

        if len(text_columns) >= 1 and len(numeric_columns) >= 1:

            fig = px.bar(
                dataframe,
                x=text_columns[0],
                y=numeric_columns[0],
                title="Business Analysis",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )