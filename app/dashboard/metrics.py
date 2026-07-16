"""
Dashboard Metrics
"""

import pandas as pd
import streamlit as st


class DashboardMetrics:

    @staticmethod
    def show_metrics(df: pd.DataFrame):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                len(df),
            )

        with col2:
            st.metric(
                "Columns",
                len(df.columns),
            )

        with col3:
            st.metric(
                "Status",
                "Success",
            )

        with col4:
            numeric_cols = len(
                df.select_dtypes(include="number").columns
            )

            st.metric(
                "Numeric Columns",
                numeric_cols,
            )