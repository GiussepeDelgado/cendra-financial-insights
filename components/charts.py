import pandas as pd
import plotly.express as px
import streamlit as st

from core.analytics import (
    get_expenses_by_category,
    get_monthly_summary,
    get_sales_by_product,
)


def render_financial_charts(
    df: pd.DataFrame,
) -> None:

    # =========================
    # EVOLUCIÓN FINANCIERA
    # =========================


    monthly = get_monthly_summary(df)

    fig_monthly = px.line(
        monthly,
        x="mes",
        y="monto",
        color="tipo",
        markers=True,
        title="Ventas y gastos por mes",
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        key="chart_monthly_evolution",
    )

    # =========================
    # GRÁFICOS SECUNDARIOS
    # =========================

    col_left, col_right = st.columns(2)

    with col_left:

        st.subheader(
            "Ventas por producto"
        )

        sales_product = get_sales_by_product(df)

        fig_products = px.bar(
            sales_product,
            x="producto",
            y="monto",
            title="Productos con mayores ventas",
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True,
            key="chart_sales_by_product",
        )

    with col_right:

        st.subheader(
            "Gastos por categoría"
        )

        expenses_category = (
            get_expenses_by_category(df)
        )

        fig_expenses = px.pie(
            expenses_category,
            names="categoria",
            values="monto",
            title="Distribución de gastos",
        )

        st.plotly_chart(
            fig_expenses,
            use_container_width=True,
            key="chart_expenses_by_category"
        )