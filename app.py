from datetime import timedelta
import pandas as pd
import streamlit as st
import plotly.express as px

from core.analytics import (
    calculate_kpis,
    calculate_commercial_kpis,
    calculate_period_comparison,
    get_monthly_summary,
    get_sales_by_product,
    get_expenses_by_category,
)
from core.insights import generate_insights
from core.loader import load_file
from core.transformer import normalize_dataframe
from core.validator import validate_dataframe

from core.analytics import (
    calculate_kpis,
    get_monthly_summary,
    get_sales_by_product,
    get_expenses_by_category,
)
from core.score import (
    calculate_cendra_score,
    classify_score,
)

from core.anomalies import (
    detect_anomalies,
)

from components.charts import (
    render_financial_charts,
)
from components.filters import (
    render_filters,
)
from components.kpis import (
    render_commercial_kpis,
    render_main_kpis,
)
from components.anomalies import (
    render_anomalies,
)

from core.loader import load_file
from core.transformer import normalize_dataframe
from core.validator import validate_dataframe

from core.risk import calculate_concentration_risk

from components.export import (
    render_export_button,
)

from components.layout import (
    apply_custom_styles,
    render_empty_state,
    render_header,
    render_section_header,
)


st.set_page_config(
    page_title="Cendra Financial Insights",
    page_icon="📊",
    layout="wide",
)

apply_custom_styles()
render_header()


uploaded_file = st.file_uploader(
    "Archivo de transacciones",
    type=["csv", "xlsx"],
    help=(
        "El archivo debe incluir las columnas: "
        "fecha, tipo, categoria, producto, "
        "cliente, cantidad y monto."
    ),
)

if not uploaded_file:
    render_empty_state()
    st.stop()


if uploaded_file:
    try:
        # 1. Cargar archivo
        df = load_file(uploaded_file)

        # 2. Normalizar
        df = normalize_dataframe(df)

        # 3. Validar
        validation = validate_dataframe(df)

        if validation["errors"]:

            for error in validation["errors"]:
                st.error(error)

            st.stop()


        if validation["warnings"]:

            with st.expander(
                "Advertencias de calidad de datos"
            ):

                for warning in validation["warnings"]:
                    st.warning(warning)

        quality_issues = (
            len(validation["errors"])
            + len(validation["warnings"])
        )

        if quality_issues == 0:
            st.success(
                "Archivo validado correctamente."
            )

        info_col1, info_col2, info_col3 = st.columns(3)

        info_col1.caption(
            f"Registros: {len(df):,}"
        )

        info_col2.caption(
            f"Desde: {df['fecha'].min():%d/%m/%Y}"
        )

        info_col3.caption(
            f"Hasta: {df['fecha'].max():%d/%m/%Y}"
        )


        # =========================
        # FILTROS
        # =========================

        filtered_df, previous_df = render_filters(df)

        

        if filtered_df.empty:
            st.warning(
                "No existen datos para los filtros seleccionados."
            )
            st.stop()


        st.caption(
            f"Analizando {len(filtered_df):,} registros "
            f"entre "
            f"{filtered_df['fecha'].min():%d/%m/%Y} "
            f"y "
            f"{filtered_df['fecha'].max():%d/%m/%Y}."
        )

        # =========================
        # KPIs
        # =========================

        kpis = calculate_kpis(filtered_df)

        commercial_kpis = calculate_commercial_kpis(
            filtered_df
        )

        cendra_score = calculate_cendra_score(
            filtered_df,
            previous_df,
        )     


        

        score_classification = classify_score(
            cendra_score["total"]
        )

        anomalies = detect_anomalies(
            filtered_df,
            threshold=2.5,
        )        

        concentration_risk = calculate_concentration_risk(
            filtered_df
        )

        comparison = calculate_period_comparison(
            filtered_df,
            previous_df,
        )

        render_section_header(
            "RESUMEN FINANCIERO",
            "Rendimiento del negocio",
            (
                "Indicadores principales del período "
                "seleccionado y su variación frente "
                "al período anterior."
            ),
        )

        render_main_kpis(
            kpis,
            comparison,
        )

        render_commercial_kpis(
            commercial_kpis,
        )
        

        insights = generate_insights(
            filtered_df,
            previous_df,
        )

        if insights:

            render_section_header(
                "INTELIGENCIA",
                "Señales del negocio",
                (
                    "Cambios relevantes detectados "
                    "frente al período anterior."
                ),
            )

            for insight in insights:

                if insight["type"] == "positive":
                    st.success(
                        f"**{insight['title']}**\n\n"
                        f"{insight['message']}"
                    )

                elif insight["type"] == "warning":
                    st.warning(
                        f"**{insight['title']}**\n\n"
                        f"{insight['message']}"
                    )

                    for insight in insights:

                        if insight["type"] == "positive":
                            st.success(
                                f"**{insight['title']}**\n\n"
                                f"{insight['message']}"
                            )

                        elif insight["type"] == "warning":
                            st.warning(
                                f"**{insight['title']}**\n\n"
                                f"{insight['message']}"
                            )

        
        # =========================
        # RIESGO DE CONCENTRACIÓN
        # =========================

        render_section_header(
            "RIESGO",
            "Concentración del negocio",
            (
                "Evalúa la dependencia respecto "
                "a clientes y productos principales."
            ),
        )

        risk_col1, risk_col2 = st.columns(2)


        with risk_col1:

            customer_level = (
                concentration_risk["customer_level"]
            )

            customer_message = (
                f"**{concentration_risk['top_customer']}** "
                f"representa el "
                f"**{concentration_risk['customer_share']:.1f}%** "
                f"de las ventas."
            )

            if customer_level == "high":
                st.error(
                    "🔴 **Alta dependencia de cliente**\n\n"
                    + customer_message
                )

            elif customer_level == "medium":
                st.warning(
                    "🟡 **Dependencia moderada de cliente**\n\n"
                    + customer_message
                )

            else:
                st.success(
                    "🟢 **Concentración de clientes saludable**\n\n"
                    + customer_message
                )


        with risk_col2:

            product_level = (
                concentration_risk["product_level"]
            )

            product_message = (
                f"**{concentration_risk['top_product']}** "
                f"representa el "
                f"**{concentration_risk['product_share']:.1f}%** "
                f"de las ventas."
            )

            if product_level == "high":
                st.error(
                    "🔴 **Alta dependencia de producto**\n\n"
                    + product_message
                )

            elif product_level == "medium":
                st.warning(
                    "🟡 **Dependencia moderada de producto**\n\n"
                    + product_message
                )

            else:
                st.success(
                    "🟢 **Concentración de productos saludable**\n\n"
                    + product_message
                )


        render_section_header(
            "MONITOREO",
            "Transacciones fuera del patrón",
            (
                "Identifica movimientos "
                "estadísticamente inusuales "
                "respecto a operaciones "
                "del mismo tipo."
            ),
        )

        render_anomalies(
            anomalies
        )


        # =========================
        # CENDRA SCORE
        # =========================

        render_section_header(
            "SALUD FINANCIERA",
            "Cendra Score",
            (
                "Resumen de rentabilidad, crecimiento, "
                "control de gastos y estabilidad."
            ),
        )

        score_col, detail_col = st.columns(
            [1, 2]
        )

        with score_col:

            total_score = cendra_score["total"]

            if total_score is not None:
                st.metric(
                    "Salud financiera",
                    f"{total_score:.1f} / 100",
                )
            else:
                st.metric(
                    "Salud financiera",
                    "Sin datos",
                )

            level = score_classification["level"]

            if level in [
                "excellent",
                "healthy",
            ]:
                st.success(
                    f"**{score_classification['status']}**\n\n"
                    f"{score_classification['message']}"
                )

            elif level == "warning":
                st.warning(
                    f"**{score_classification['status']}**\n\n"
                    f"{score_classification['message']}"
                )

            elif level == "risk":
                st.error(
                    f"**{score_classification['status']}**\n\n"
                    f"{score_classification['message']}"
                )

            else:
                st.info(
                    f"**{score_classification['status']}**\n\n"
                    f"{score_classification['message']}"
                )

            st.caption(
                f"Cobertura del análisis: "
                f"{cendra_score['coverage']:.0f}%"
            )


        with detail_col:

            score_dimensions = {
                "Rentabilidad": (
                    cendra_score["profitability"]
                ),
                "Crecimiento": (
                    cendra_score["growth"]
                ),
                "Control de gastos": (
                    cendra_score["expense_control"]
                ),
                "Estabilidad": (
                    cendra_score["stability"]
                ),
            }

            score_data = pd.DataFrame([
                {
                    "Dimensión": dimension,
                    "Puntuación": value,
                }
                for dimension, value
                in score_dimensions.items()
                if value is not None
            ])

            if not score_data.empty:

                fig_score = px.bar(
                    score_data,
                    x="Puntuación",
                    y="Dimensión",
                    orientation="h",
                    range_x=[0, 100],
                    title="Componentes del Score",
                )

                st.plotly_chart(
                    fig_score,
                    use_container_width=True,
                    key="chart_cendra_score_components",
                )

            else:
                st.info(
                    "No existen dimensiones suficientes "
                    "para mostrar el Score."
                )

        with st.expander(
            "Cómo se calcula el Cendra Score"
        ):

            st.markdown(
                """
                El Cendra Score resume la salud financiera
                utilizando las dimensiones disponibles:

                - **Rentabilidad:** desempeño del margen.
                - **Crecimiento:** variación de ventas frente
                al período anterior comparable.
                - **Control de gastos:** evolución de gastos
                frente al período anterior.
                - **Estabilidad:** variabilidad de ventas
                mensuales.

                Cuando una dimensión no dispone de datos
                suficientes, se excluye del cálculo y los
                pesos disponibles se normalizan.

                **Nota:** el Score es un indicador heurístico
                de apoyo y no constituye asesoría financiera.
                """
            )        

        # =========================
        # REPORTE EJECUTIVO
        # =========================

        render_export_button(
            df=filtered_df,
            kpis=kpis,
            commercial_kpis=commercial_kpis,
            cendra_score=cendra_score,
            score_classification=score_classification,
            concentration_risk=concentration_risk,
            insights=insights,
        )        

        st.divider()

        # =========================
        # EVOLUCIÓN MENSUAL
        # =========================

        st.divider()

        render_section_header(
            "TENDENCIAS",
            "Evolución financiera",
            (
                "Explora el comportamiento temporal "
                "de ventas, gastos y composición "
                "del negocio."
            ),
        )

        render_financial_charts(
            filtered_df
        )

        # =========================
        # TABLA
        # =========================

        st.divider()

        render_section_header(
            "DETALLE",
            "Transacciones",
            (
                "Consulta los registros incluidos "
                "en el análisis actual."
            ),
        )

        st.dataframe(
            filtered_df,
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
            },
        )

    except Exception as error:
        st.error(
            f"No se pudo procesar el archivo: {error}"
        )