from textwrap import dedent
import pandas as pd
import streamlit as st

from services.report_service import (
    generate_excel_report,
)


def render_export_button(
    df: pd.DataFrame,
    kpis: dict,
    commercial_kpis: dict,
    cendra_score: dict,
    score_classification: dict,
    concentration_risk: dict,
    insights: list[dict],
) -> None:

    report = generate_excel_report(
        df=df,
        kpis=kpis,
        commercial_kpis=commercial_kpis,
        cendra_score=cendra_score,
        score_classification=score_classification,
        concentration_risk=concentration_risk,
        insights=insights,
    )

    export_html = """
    <div class="export-card"><div class="export-icon">↓</div><div class="export-content"><div class="export-eyebrow">REPORTE EJECUTIVO</div><div class="export-title">Lleva tu análisis contigo</div><div class="export-description">Descarga indicadores, señales, riesgos y transacciones del período seleccionado.</div></div></div>
    """

    st.markdown(
        export_html,
        unsafe_allow_html=True,
    )

    st.download_button(
        label="Descargar reporte Cendra",
        data=report,
        file_name="reporte_cendra.xlsx",
        mime=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
        type="primary",
    )