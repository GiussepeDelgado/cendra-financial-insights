import streamlit as st


def format_delta(
    value: float | None,
) -> str:

    if value is None:
        return "Sin histórico"

    sign = "+" if value >= 0 else ""

    return f"{sign}{value:.1f}%"


def get_delta_class(
    value: float | None,
    inverse: bool = False,
) -> str:

    if value is None:
        return "neutral"

    is_positive = value >= 0

    if inverse:
        is_positive = not is_positive

    return (
        "positive"
        if is_positive
        else "negative"
    )


def render_main_kpis(
    kpis: dict,
    comparison: dict,
) -> None:

    sales_delta = comparison["sales"]
    expenses_delta = comparison["expenses"]
    profit_delta = comparison["profit"]
    margin_delta = comparison["margin"]

    margin_text = (
        f"{margin_delta:+.1f} pp"
        if margin_delta is not None
        else "Sin histórico"
    )

    html = f"""
<div class="kpi-grid"><div class="kpi-card"><div class="kpi-top"><span class="kpi-label">VENTAS</span><span class="kpi-dot"></span></div><div class="kpi-value">S/ {kpis['sales']:,.2f}</div><div class="kpi-delta {get_delta_class(sales_delta)}">{format_delta(sales_delta)} <span>vs. período anterior</span></div></div><div class="kpi-card"><div class="kpi-top"><span class="kpi-label">GASTOS</span><span class="kpi-dot"></span></div><div class="kpi-value">S/ {kpis['expenses']:,.2f}</div><div class="kpi-delta {get_delta_class(expenses_delta, inverse=True)}">{format_delta(expenses_delta)} <span>vs. período anterior</span></div></div><div class="kpi-card"><div class="kpi-top"><span class="kpi-label">UTILIDAD</span><span class="kpi-dot"></span></div><div class="kpi-value">S/ {kpis['profit']:,.2f}</div><div class="kpi-delta {get_delta_class(profit_delta)}">{format_delta(profit_delta)} <span>vs. período anterior</span></div></div><div class="kpi-card featured"><div class="kpi-top"><span class="kpi-label">MARGEN</span><span class="kpi-dot"></span></div><div class="kpi-value">{kpis['margin']:.1f}%</div><div class="kpi-delta {get_delta_class(margin_delta)}">{margin_text} <span>vs. período anterior</span></div></div></div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def render_commercial_kpis(
    commercial_kpis: dict,
) -> None:

    st.markdown(
        "### Indicadores comerciales"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Ticket promedio",
        (
            f"S/ "
            f"{commercial_kpis['average_ticket']:,.2f}"
        ),
    )

    col2.metric(
        "N.º de ventas",
        commercial_kpis["number_of_sales"],
    )

    col3.metric(
        "Producto líder",
        commercial_kpis["top_product"],
    )

    col4.metric(
        "Cliente principal",
        commercial_kpis["top_customer"],
    )