"""
Home Page
"""

import streamlit as st


class HomePage:

    @staticmethod
    def show():

        st.title("📊 InsightIQ")

        st.subheader(
            "AI-Powered Business Intelligence Platform"
        )

        st.markdown("---")

        st.markdown(
            """
Welcome to **InsightIQ**.

Analyze your business data using natural language,
interactive dashboards, and AI-generated SQL.

No SQL knowledge required.
"""
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                """
### 🤖 AI Chat

- Ask questions in plain English
- AI generates SQL
- Interactive charts
- Export results
"""
            )

        with col2:

            st.success(
                """
### 📊 Executive Dashboard

- KPI Cards
- Revenue Trends
- Product Analysis
- Regional Insights
"""
            )

        st.markdown("---")

        st.subheader("🚀 Technologies")

        tech1, tech2, tech3, tech4, tech5 = st.columns(5)

        with tech1:
            st.metric("🐍", "Python")

        with tech2:
            st.metric("🗄️", "PostgreSQL")

        with tech3:
            st.metric("🤖", "Gemini")

        with tech4:
            st.metric("📈", "Plotly")

        with tech5:
            st.metric("⚡", "Streamlit")

        st.markdown("---")

        st.caption(
            "InsightIQ v1.0 • AI Business Intelligence Platform"
        )