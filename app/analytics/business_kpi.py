"""
Business KPI Calculator
"""


class BusinessKPI:

    @staticmethod
    def calculate(
        revenue,
        orders,
        customers,
        products,
    ):

        average_order_value = (
            revenue / orders
            if orders
            else 0
        )

        orders_per_customer = (
            orders / customers
            if customers
            else 0
        )

        revenue_per_product = (
            revenue / products
            if products
            else 0
        )

        return {
            "Average Order Value": average_order_value,
            "Orders per Customer": orders_per_customer,
            "Revenue per Product": revenue_per_product,
        }