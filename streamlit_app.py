"""
InsightIQ AI Business Intelligence

Main Streamlit Application
"""

import streamlit as st

from app.dashboard.executive_dashboard import ExecutiveDashboard
from app.dashboard.metrics import DashboardMetrics
from app.insights.insight_generator import InsightGenerator
from app.pages.home import HomePage
from app.reports.pdf_generator import PDFGenerator
from app.services.ai_query_service import AIQueryService
from app.visualization.chart_generator import ChartGenerator
from app.ai.query_interpreter import QueryInterpreter

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="InsightIQ AI",
    page_icon="📊",
    layout="wide",
)

# =====================================================
# Sample Questions
# =====================================================

SAMPLE_QUESTIONS = [
    "Top 10 products by revenue",
    "Top 10 customers by orders",
    "Revenue by territory",
    "Products with highest sales",
    "Monthly sales trend",
    "Revenue by category",
]

# =====================================================
# Session State
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = []

# =====================================================
# Sidebar
# =====================================================

selected_question = None

with st.sidebar:

    st.title("📊 InsightIQ")

    st.markdown("---")

    mode = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🤖 AI Chat",
            "📊 Dashboard",
        ],
    )

    st.markdown("---")

    st.subheader("🕒 Recent Queries")

    if st.session_state.recent_queries:

        for query in reversed(
            st.session_state.recent_queries
        ):

            st.write(f"• {query}")

    else:

        st.caption("No recent queries")

    st.markdown("---")

    st.subheader("💡 Sample Questions")

    for sample in SAMPLE_QUESTIONS:

        if st.button(
            sample,
            use_container_width=True,
        ):

            selected_question = sample

    st.markdown("---")

    st.subheader("🗄️ Data Warehouse")

    st.success("AdventureWorks")

    st.markdown("---")

    st.subheader("🤖 AI Model")

    st.info("Gemini 2.5 Flash")

    st.markdown("---")

    st.subheader("⚙️ Technology Stack")

    st.markdown("""
- Python
- Streamlit
- PostgreSQL
- SQL Server
- Plotly
- Google Gemini
""")

    st.markdown("---")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages.clear()
        st.session_state.recent_queries.clear()

        st.rerun()

    st.markdown("---")

    st.caption("InsightIQ v1.0")
    # =====================================================
# Navigation
# =====================================================

if mode == "🏠 Home":

    HomePage.show()

    st.stop()

if mode == "📊 Dashboard":

    ExecutiveDashboard.show()

    st.stop()

# =====================================================
# Main Page
# =====================================================

st.title("📊 InsightIQ AI Business Intelligence")

st.markdown(
    "Ask business questions in natural language."
)

# =====================================================
# Previous Conversation
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] != "assistant":
            continue

        # ----------------------------------------
        # Generated SQL
        # ----------------------------------------

        if "sql" in message:

            st.subheader("Generated SQL")

            st.code(
                message["sql"],
                language="sql",
            )

        # ----------------------------------------
        # Results
        # ----------------------------------------

        if "data" not in message:
            continue

        dataframe = message["data"]

        st.subheader("Results")

        DashboardMetrics.show_metrics(
            dataframe
        )

        # Empty Result Handling

        if dataframe.empty:

            st.warning(
                """
No records matched this query.
Try another business question.
"""
            )

            continue

        st.dataframe(
            dataframe,
            use_container_width=True,
        )

        # ----------------------------------------
        # Download CSV
        # ----------------------------------------

        csv = dataframe.to_csv(
            index=False,
        )

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            key=f"csv_{id(message)}",
        )

        # ----------------------------------------
        # Smart Chart
        # ----------------------------------------

        ChartGenerator.show_chart(
            dataframe,
            message.get(
                "question",
                "",
            ),
        )

        # ----------------------------------------
        # AI Business Insight
        # ----------------------------------------

        if "insight" in message:

            st.markdown("---")

            st.subheader(
                "💡 AI Business Insight"
            )

            st.success(
                message["insight"]
            )

        # ----------------------------------------
        # Export PDF
        # ----------------------------------------

        if "insight" in message:

            pdf = PDFGenerator.generate(
                question=message.get(
                    "question",
                    "",
                ),
                sql=message.get(
                    "sql",
                    "",
                ),
                dataframe=dataframe,
                insight=message[
                    "insight"
                ],
            )

            st.download_button(
                label="📄 Export PDF Report",
                data=pdf,
                file_name="InsightIQ_Report.pdf",
                mime="application/pdf",
                key=f"pdf_{id(message)}",
            )
            # =====================================================
# Chat Input
# =====================================================

typed_question = st.chat_input(
    "Ask a business question..."
)

question = typed_question

if selected_question:
    question = selected_question

# =====================================================
# Execute Query
# =====================================================

if question:

    # ----------------------------------------
    # Save User Message
    # ----------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    st.session_state.recent_queries.append(
        question
    )

    st.session_state.recent_queries = (
        st.session_state.recent_queries[-5:]
    )

    with st.chat_message("user"):

        st.markdown(question)

    service = AIQueryService()

    try:

        with st.spinner(
            "🤖 Understanding question..."
        ):

            sql, dataframe = service.ask(
                question
            )

        with st.chat_message("assistant"):

            st.markdown(
                "Here are your results."
            )
            # ----------------------------------------
# AI Interpretation
# ----------------------------------------

            interpretation = QueryInterpreter.interpret(
                question
            )

            st.subheader("🧠 AI Interpretation")

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"""
            **Intent**

            {interpretation["intent"]}

            **Metric**

            {interpretation["metric"]}
            """
                )

            with col2:

                filters = (
                    ", ".join(interpretation["filters"])
                    if interpretation["filters"]
                    else "None"
                )

                st.info(
                    f"""
            **Filters**

            {filters}

            **Visualization**

            {interpretation["visualization"]}
            """
                )
                st.progress(
                interpretation["confidence"] / 100
            )

            st.caption(
                f"AI Confidence: {interpretation['confidence']}%"
            )

            # Existing line
            st.markdown("---")

            # Then Generated SQL starts

            st.subheader("Generated SQL")

            st.markdown("---")

            # ----------------------------------------
            # Generated SQL
            # ----------------------------------------

            st.subheader(
                "Generated SQL"
            )

            st.code(
                sql,
                language="sql",
            )

            # ----------------------------------------
            # Results
            # ----------------------------------------

            st.subheader(
                "Results"
            )

            DashboardMetrics.show_metrics(
                dataframe
            )

            # ----------------------------------------
            # Empty Result
            # ----------------------------------------

            if dataframe.empty:

                st.warning(
                    """
No records matched your query.

Try another business question.
"""
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": "No records found.",
                        "sql": sql,
                        "data": dataframe,
                        "question": question,
                    }
                )

                service.close()

                st.stop()

            # ----------------------------------------
            # Data
            # ----------------------------------------

            st.dataframe(
                dataframe,
                use_container_width=True,
            )

            # ----------------------------------------
            # CSV Export
            # ----------------------------------------

            csv = dataframe.to_csv(
                index=False
            )

            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv",
                key=f"csv_{len(st.session_state.messages)}",
            )

            # ----------------------------------------
            # Smart Chart
            # ----------------------------------------

            ChartGenerator.show_chart(
                dataframe,
                question,
            )

            # ----------------------------------------
            # AI Insight
            # ----------------------------------------

            insight_generator = InsightGenerator()

            insight = (
                insight_generator.generate_insight(
                    question,
                    dataframe,
                )
            )

            st.markdown("---")

            st.subheader(
                "💡 AI Business Insight"
            )

            st.success(
                insight
            )

            # ----------------------------------------
            # PDF Export
            # ----------------------------------------

            pdf = PDFGenerator.generate(
                question=question,
                sql=sql,
                dataframe=dataframe,
                insight=insight,
                alerts=None,
            )

            st.download_button(
                label="📄 Export PDF Report",
                data=pdf,
                file_name="InsightIQ_Report.pdf",
                mime="application/pdf",
                key=f"pdf_{len(st.session_state.messages)}",
            )

        # ----------------------------------------
        # Save Assistant Message
        # ----------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "Here are your results.",
                "sql": sql,
                "data": dataframe,
                "question": question,
                "insight": insight,
            }
        )
    except Exception as error:

        error_message = str(error)

        with st.chat_message("assistant"):

            # ----------------------------------------
            # Gemini Quota Error
            # ----------------------------------------

            if (
                "RESOURCE_EXHAUSTED" in error_message
                or "quota" in error_message.lower()
            ):

                st.error(
                    """
⚠ Gemini API quota exceeded.

Please try again later or use another API key.
"""
                )

            # ----------------------------------------
            # Database Error
            # ----------------------------------------

            elif (
                "connection" in error_message.lower()
                or "postgres" in error_message.lower()
                or "sqlalchemy" in error_message.lower()
                or "psycopg2" in error_message.lower()
            ):

                st.error(
                    """
⚠ Unable to connect to the database.

Please ensure PostgreSQL is running.
"""
                )

            # ----------------------------------------
            # Invalid SQL
            # ----------------------------------------

            elif (
                "syntax" in error_message.lower()
                or "column" in error_message.lower()
                or "relation" in error_message.lower()
            ):

                st.error(
                    """
⚠ The generated SQL could not be executed.

Please try rephrasing your question.
"""
                )

            # ----------------------------------------
            # Generic Error
            # ----------------------------------------

            else:

                st.error(
                    f"⚠ {error_message}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )

    finally:

        service.close()