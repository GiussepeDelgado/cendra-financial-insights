import pandas as pd
import streamlit as st


def render_anomalies(
    anomalies: pd.DataFrame,
) -> None:

    if anomalies.empty:

        st.success(
            "No se detectaron transacciones "
            "fuera del patrón estadístico."
        )

        return

    anomaly_count = len(anomalies)

    total_amount = (
        anomalies["monto"].sum()
    )

    max_deviation = (
        anomalies["desviacion"].max()
    )

    # =========================
    # RESUMEN
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Anomalías detectadas",
        anomaly_count,
    )

    col2.metric(
        "Monto involucrado",
        f"S/ {total_amount:,.2f}",
    )

    col3.metric(
        "Mayor desviación",
        f"{max_deviation:.1f}σ",
    )

    # =========================
    # MENSAJE
    # =========================

    st.warning(
        f"Se detectaron {anomaly_count} "
        f"transacciones con comportamiento "
        f"inusual respecto a operaciones "
        f"del mismo tipo."
    )

    # =========================
    # TABLA
    # =========================

    display_columns = [
        "fecha",
        "tipo",
        "categoria",
        "producto",
        "cliente",
        "monto",
        "desviacion",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in anomalies.columns
    ]

    st.dataframe(
        anomalies[available_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "fecha": st.column_config.DateColumn(
                "Fecha",
                format="DD/MM/YYYY",
            ),
            "monto": st.column_config.NumberColumn(
                "Monto",
                format="S/ %.2f",
            ),
            "desviacion": (
                st.column_config.NumberColumn(
                    "Desviación",
                    format="%.2f σ",
                )
            ),
        },
    )