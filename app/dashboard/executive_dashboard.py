"""
Executive Dashboard
"""

import plotly.express as px
import streamlit as st

from app.analytics.dashboard_service import DashboardService
from app.analytics.business_alerts import BusinessAlerts
from app.analytics.business_kpi import BusinessKPI
from app.analytics.business_score import BusinessScore


class ExecutiveDashboard:

    @staticmethod
    def show():

        st.title("📊 InsightIQ Executive Dashboard")

        st.caption(
            "AI-Powered Business Intelligence Dashboard"
        )

        st.markdown("---")

        service = DashboardService()

        try:

            # ==========================================
            # Dashboard Filters
            # ==========================================

            years = ["All"] + [
                str(year)
                for year in service.get_years()
            ]

            regions = ["All"] + service.get_regions()

            categories = (
                ["All"]
                + service.get_categories()
            )

            filter1, filter2, filter3 = st.columns(3)

            with filter1:

                selected_year = st.selectbox(
                    "📅 Year",
                    years,
                )

            with filter2:

                selected_region = st.selectbox(
                    "🌍 Region",
                    regions,
                )

            with filter3:

                selected_category = st.selectbox(
                    "🛒 Category",
                    categories,
                )

            st.markdown("---")

            # ==========================================
            # KPI Cards
            # ==========================================

            revenue = service.total_revenue(
                selected_year,
                selected_region,
                selected_category,
            )

            orders = service.total_orders(
                selected_year,
                selected_region,
                selected_category,
            )

            customers = service.total_customers(
                selected_year,
                selected_region,
                selected_category,
            )

            products = service.total_products(
                selected_year,
                selected_region,
                selected_category,
            )
            kpis = BusinessKPI.calculate(
            revenue,
            orders,
            customers,
            products,
            )
            score, status = BusinessScore.calculate(
                    revenue,
                    orders,
                    customers,
                    products,
                )
            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "💰 Revenue",
                    f"${revenue:,.0f}",
                )

            with col2:

                st.metric(
                    "👥 Customers",
                    f"{customers:,}",
                )

            with col3:

                st.metric(
                    "📦 Orders",
                    f"{orders:,}",
                )

            with col4:

                st.metric(
                    "🛒 Products",
                    f"{products:,}",
                )
                # ==========================================
# Executive KPIs
# ==========================================

            kpi1, kpi2, kpi3 = st.columns(3)

            with kpi1:

                st.metric(
                    "💰 Avg Order Value",
                    f"${kpis['Average Order Value']:,.2f}",
                )

            with kpi2:

                st.metric(
                    "👥 Orders / Customer",
                    f"{kpis['Orders per Customer']:.2f}",
                )

            with kpi3:

                st.metric(
                    "📦 Revenue / Product",
                    f"${kpis['Revenue per Product']:,.2f}",
                )

            st.markdown("---")

            st.subheader("📈 Business Health Score")

            st.metric(
                "Overall Business Score",
                f"{score}/100",
                status,
            )

            st.markdown("---")

                        # ==========================================
            # Executive Summary
            # ==========================================

            best_product = service.best_product(
                selected_year,
                selected_region,
                selected_category,
            )

            best_category = service.best_category(
                selected_year,
                selected_region,
                selected_category,
            )

            best_region = service.best_region(
                selected_year,
                selected_region,
                selected_category,
            )


            recommendation = (
                service.executive_recommendation(
                    selected_year,
    selected_region,
    selected_category,
                )
            )
            alerts = BusinessAlerts.generate(
                revenue,
                best_product,
                best_category,
                best_region,
            )

            st.subheader("🚨 Business Alerts")

            for alert in alerts:

                st.info(alert)

            st.markdown("---")



            st.subheader("📌 Executive Summary")

            summary1, summary2 = st.columns(2)

            with summary1:

                st.success(
                    f"""
### 🏆 Top Product

**{best_product['product_name']}**

Revenue: ${best_product['revenue']:,.0f}
"""
                )

                st.info(
                    f"""
### 🥧 Best Category

**{best_category['category']}**

Revenue: ${best_category['revenue']:,.0f}
"""
                )

            with summary2:

                st.info(
                    f"""
### 🌍 Top Region

**{best_region['region']}**

Revenue: ${best_region['revenue']:,.0f}
"""
                )

                st.warning(
                    f"""
### 💡 Recommendation

{recommendation}
"""
                )

            st.markdown("---")

            # ==========================================
            # First Row Charts
            # ==========================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("📈 Monthly Revenue Trend")

                monthly_df = service.monthly_revenue(
                    selected_year,
                    selected_region,
                    selected_category,
                )

                fig = px.line(
                    monthly_df,
                    x="Period",
                    y="revenue",
                    markers=True,
                    title="Monthly Revenue",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            with col2:

                st.subheader("🏆 Top 10 Products")

                top_products = service.top_products(
                    selected_year,
                    selected_region,
                    selected_category,
                )

                fig = px.bar(
                    top_products,
                    x="revenue",
                    y="product_name",
                    orientation="h",
                    title="Top Products",
                )

                fig.update_layout(
                    yaxis=dict(
                        autorange="reversed"
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            st.markdown("---")
                        # ==========================================
            # Second Row Charts
            # ==========================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("🌍 Revenue by Region")

                territory_df = service.revenue_by_territory(
                    selected_year,
                    selected_region,
                    selected_category,
                )

                fig = px.bar(
                    territory_df,
                    x="region",
                    y="revenue",
                    title="Revenue by Region",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            with col2:

                st.subheader("🥧 Revenue by Category")

                category_df = service.revenue_by_category(
                    selected_year,
                    selected_region,
                    selected_category,
                )

                fig = px.pie(
                    category_df,
                    names="category",
                    values="revenue",
                    hole=0.45,
                    title="Revenue by Category",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            st.markdown("---")

            # ==========================================
            # Raw Dashboard Data
            # ==========================================

            with st.expander(
                "📋 View Dashboard Data"
            ):

                st.write("Monthly Revenue")

                st.dataframe(
                    monthly_df,
                    use_container_width=True,
                )

                st.write("Top Products")

                st.dataframe(
                    top_products,
                    use_container_width=True,
                )

                st.write("Revenue by Region")

                st.dataframe(
                    territory_df,
                    use_container_width=True,
                )

                st.write("Revenue by Category")

                st.dataframe(
                    category_df,
                    use_container_width=True,
                )

        finally:

            service.close()