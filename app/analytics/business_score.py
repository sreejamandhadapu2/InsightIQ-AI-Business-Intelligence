"""
Business Health Score
"""


class BusinessScore:

    @staticmethod
    def calculate(
        revenue,
        orders,
        customers,
        products,
    ):

        score = 0

        if revenue > 10000000:
            score += 30
        elif revenue > 5000000:
            score += 20
        else:
            score += 10

        if orders > 10000:
            score += 25
        elif orders > 5000:
            score += 15
        else:
            score += 10

        if customers > 5000:
            score += 25
        elif customers > 2000:
            score += 15
        else:
            score += 10

        if products > 100:
            score += 20
        elif products > 50:
            score += 15
        else:
            score += 10

        if score >= 85:
            status = "🟢 Excellent"

        elif score >= 65:
            status = "🟡 Good"

        else:
            status = "🔴 Needs Attention"

        return score, status