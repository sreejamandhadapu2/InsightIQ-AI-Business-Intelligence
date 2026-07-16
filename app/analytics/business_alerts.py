"""
Business Alerts
"""


class BusinessAlerts:

    @staticmethod
    def generate(
        revenue,
        best_product,
        best_category,
        best_region,
    ):

        alerts = []

        # Revenue Alert
        if revenue >= 10000000:

            alerts.append(
                f"💰 Excellent revenue performance (${revenue:,.0f})."
            )

        elif revenue >= 5000000:

            alerts.append(
                f"📈 Strong revenue performance (${revenue:,.0f})."
            )

        else:

            alerts.append(
                f"⚠ Revenue is relatively low (${revenue:,.0f})."
            )

        # Product Alert
        alerts.append(
            f"🏆 '{best_product['product_name']}' is the top-selling product."
        )

        # Category Alert
        alerts.append(
            f"🥇 '{best_category['category']}' is the highest revenue category."
        )

        # Region Alert
        alerts.append(
            f"🌍 '{best_region['region']}' is the strongest performing region."
        )

        # Recommendation
        alerts.append(
            "💡 Focus marketing and inventory on the leading product and category while expanding successful regional strategies."
        )

        return alerts