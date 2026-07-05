import pandas as pd

from core.analytics import calculate_kpis


def generate_insights(
    current_df: pd.DataFrame,
    previous_df: pd.DataFrame,
) -> list[dict]:

    current = calculate_kpis(current_df)
    previous = calculate_kpis(previous_df)

    insights = []

    # Ventas
    if previous["sales"] > 0:
        sales_change = (
            (current["sales"] - previous["sales"])
            / previous["sales"]
            * 100
        )

        if sales_change >= 10:
            insights.append({
                "type": "positive",
                "title": "Crecimiento de ventas",
                "message": (
                    f"Las ventas aumentaron "
                    f"{sales_change:.1f}% "
                    f"respecto al período anterior."
                ),
            })

        elif sales_change <= -10:
            insights.append({
                "type": "warning",
                "title": "Caída de ventas",
                "message": (
                    f"Las ventas disminuyeron "
                    f"{abs(sales_change):.1f}% "
                    f"respecto al período anterior."
                ),
            })

    # Gastos
    if previous["expenses"] > 0:
        expense_change = (
            (current["expenses"] - previous["expenses"])
            / previous["expenses"]
            * 100
        )

        if expense_change >= 15:
            insights.append({
                "type": "warning",
                "title": "Incremento de gastos",
                "message": (
                    f"Los gastos aumentaron "
                    f"{expense_change:.1f}%."
                ),
            })

    # Margen
    margin_change = (
        current["margin"]
        - previous["margin"]
    )

    if margin_change <= -5:
        insights.append({
            "type": "warning",
            "title": "Deterioro del margen",
            "message": (
                f"El margen cayó "
                f"{abs(margin_change):.1f} "
                f"puntos porcentuales."
            ),
        })

    elif margin_change >= 5:
        insights.append({
            "type": "positive",
            "title": "Mejora del margen",
            "message": (
                f"El margen aumentó "
                f"{margin_change:.1f} "
                f"puntos porcentuales."
            ),
        })

    return insights