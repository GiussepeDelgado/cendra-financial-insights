import streamlit as st


def apply_custom_styles() -> None:
    st.markdown(
        """
        <style>

        /* =========================
           CONTENEDOR PRINCIPAL
        ========================= */

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* =========================
           HERO CENDRA
        ========================= */

        .cendra-hero {
            position: relative;
            overflow: hidden;

            display: grid;
            grid-template-columns: 1.6fr 0.7fr;
            align-items: center;
            gap: 2rem;

            min-height: 320px;
            margin-bottom: 2rem;
            padding: 3rem;

            border-radius: 24px;

            background:
                radial-gradient(
                    circle at 85% 20%,
                    rgba(56, 189, 248, 0.22),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(16, 185, 129, 0.18),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #07111f 0%,
                    #0b1f33 55%,
                    #102a43 100%
                );

            border:
                1px solid rgba(255, 255, 255, 0.10);

            box-shadow:
                0 24px 60px rgba(0, 0, 0, 0.18);
        }

        .cendra-hero::before {
            content: "";

            position: absolute;

            width: 260px;
            height: 260px;

            right: -80px;
            top: -100px;

            border-radius: 50%;

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }

        .cendra-hero::after {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            right: 40px;
            bottom: -120px;

            border-radius: 50%;

            background:
                rgba(56, 189, 248, 0.08);
        }

        .cendra-hero-content {
            position: relative;
            z-index: 2;
        }

        .cendra-badge {
            display: inline-block;

            margin-bottom: 1.2rem;
            padding: 0.45rem 0.8rem;

            border-radius: 999px;

            background:
                rgba(56, 189, 248, 0.12);

            border:
                1px solid rgba(56, 189, 248, 0.25);

            color: #7dd3fc;

            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
        }

        .cendra-title {
            margin: 0;

            color: #ffffff;

            font-size:
                clamp(3rem, 7vw, 5.5rem);

            font-weight: 800;

            line-height: 0.95;

            letter-spacing: -0.06em;
        }

        .cendra-subtitle {
            max-width: 680px;

            margin:
                1.2rem 0
                0.8rem 0;

            color:
                rgba(255, 255, 255, 0.92);

            font-size:
                clamp(1.3rem, 2.5vw, 2rem);

            font-weight: 700;

            line-height: 1.2;
        }

        .cendra-description {
            max-width: 620px;

            margin-top: 1rem;

            color:
                rgba(255, 255, 255, 0.65);

            font-size: 1.05rem;
            line-height: 1.65;
        }

        .cendra-features {
            display: flex;
            flex-wrap: wrap;

            gap: 0.6rem;

            margin-top: 1.5rem;
        }

        .cendra-features span {
            padding:
                0.5rem
                0.8rem;

            border-radius: 8px;

            background:
                rgba(255, 255, 255, 0.07);

            border:
                1px solid rgba(255, 255, 255, 0.08);

            color:
                rgba(255, 255, 255, 0.78);

            font-size: 0.82rem;
        }

        .cendra-hero-visual {
            position: relative;
            z-index: 2;

            display: flex;
            justify-content: center;
        }

        .hero-score-card {
            width: 100%;
            max-width: 230px;

            padding: 1.8rem;

            border-radius: 20px;

            background:
                rgba(255, 255, 255, 0.08);

            border:
                1px solid rgba(255, 255, 255, 0.12);

            backdrop-filter: blur(12px);

            box-shadow:
                0 20px 40px rgba(0, 0, 0, 0.20);
        }

        .hero-score-label {
            color:
                rgba(255, 255, 255, 0.55);

            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.12em;
        }

        .hero-score-value {
            margin:
                0.8rem 0
                0.4rem 0;

            color: #ffffff;

            font-size: 3.4rem;
            font-weight: 700;

            line-height: 1;
        }

        .hero-score-status {
            color: #6ee7b7;

            font-size: 0.82rem;
            font-weight: 600;
        }

        /* =========================
           KPI CARDS
        ========================= */

        .kpi-grid {
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 1rem;

            margin:
                1.2rem 0
                2rem 0;
        }

        .kpi-card {
            position: relative;
            overflow: hidden;

            padding: 1.35rem;

            border-radius: 16px;

            background:
                rgba(120, 120, 120, 0.055);

            border:
                1px solid rgba(120, 120, 120, 0.16);

            transition:
                transform 0.18s ease,
                border-color 0.18s ease,
                box-shadow 0.18s ease;
        }

        .kpi-card:hover {
            transform:
                translateY(-3px);

            border-color:
                rgba(14, 165, 233, 0.30);

            box-shadow:
                0 14px 30px rgba(0, 0, 0, 0.08);
        }

        .kpi-card.featured {
            background:
                linear-gradient(
                    135deg,
                    rgba(14, 165, 233, 0.10),
                    rgba(16, 185, 129, 0.08)
                );

            border-color:
                rgba(14, 165, 233, 0.22);
        }

        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .kpi-label {
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.10em;
            opacity: 0.58;
        }

        .kpi-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;

            background: #0ea5e9;

            box-shadow:
                0 0 0 5px rgba(14, 165, 233, 0.10);
        }

        .kpi-value {
            margin-top: 0.8rem;

            font-size:
                clamp(1.35rem, 2vw, 2rem);

            font-weight: 750;

            letter-spacing: -0.04em;
        }

        .kpi-delta {
            margin-top: 0.65rem;

            font-size: 0.78rem;
            font-weight: 650;
        }

        .kpi-delta span {
            margin-left: 0.2rem;

            font-weight: 400;

            opacity: 0.58;
        }

        .kpi-delta.positive {
            color: #10b981;
        }

        .kpi-delta.negative {
            color: #ef4444;
        }

        .kpi-delta.neutral {
            opacity: 0.60;
        }

        /* =========================
           SECTION HEADERS
        ========================= */

        .section-header {
            margin:
                2.4rem 0
                1rem 0;
        }

        .section-eyebrow {
            margin-bottom: 0.3rem;

            color: #0ea5e9;

            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 750;

            letter-spacing: -0.025em;
        }

        .section-description {
            max-width: 720px;

            margin-top: 0.3rem;

            font-size: 0.9rem;

            opacity: 0.62;
        }

        /* =========================
           EXPORT CARD
        ========================= */

        .export-card {
            display: flex;
            align-items: center;

            gap: 1.2rem;

            margin-top: 0.5rem;
            margin-bottom: 0.8rem;

            padding: 1.4rem 1.5rem;

            border-radius: 16px;

            background:
                linear-gradient(
                    135deg,
                    rgba(14, 165, 233, 0.08),
                    rgba(16, 185, 129, 0.08)
                );

            border:
                1px solid rgba(14, 165, 233, 0.18);
        }

        .export-icon {
            display: flex;
            align-items: center;
            justify-content: center;

            min-width: 52px;
            height: 52px;

            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #0284c7,
                    #0f766e
                );

            color: white;

            font-size: 1.5rem;
            font-weight: 700;

            box-shadow:
                0 10px 24px rgba(2, 132, 199, 0.20);
        }

        .export-content {
            flex: 1;
        }

        .export-eyebrow {
            margin-bottom: 0.25rem;

            color: #0284c7;

            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
        }

        .export-title {
            font-size: 1.15rem;
            font-weight: 700;
        }

        .export-description {
            margin-top: 0.25rem;

            color:
                rgba(120, 120, 120, 0.95);

            font-size: 0.88rem;
            line-height: 1.5;
        }

        .stDownloadButton button[kind="primary"] {
            min-height: 3.2rem;

            border: none;

            border-radius: 12px;

            font-size: 0.95rem;
            font-weight: 700;

            box-shadow:
                0 10px 25px rgba(2, 132, 199, 0.18);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }

        .stDownloadButton button[kind="primary"]:hover {
            transform:
                translateY(-2px);

            box-shadow:
                0 14px 30px rgba(2, 132, 199, 0.25);
        }

        /* =========================
           OTROS
        ========================= */

        [data-testid="stMetric"] {
            background:
                rgba(120, 120, 120, 0.06);

            border:
                1px solid rgba(120, 120, 120, 0.16);

            padding: 1rem;

            border-radius: 12px;
        }

        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }

        [data-testid="stSidebar"] {
            border-right:
                1px solid rgba(120, 120, 120, 0.14);
        }

        /* =========================
           RESPONSIVE
        ========================= */

        @media (max-width: 1000px) {

            .kpi-grid {
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 800px) {

            .cendra-hero {
                grid-template-columns: 1fr;

                padding: 2rem;
            }

            .cendra-hero-visual {
                justify-content: flex-start;
            }

            .hero-score-card {
                max-width: 100%;
            }
        }

        @media (max-width: 600px) {

            .kpi-grid {
                grid-template-columns: 1fr;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:

    hero_html = """
<div class="cendra-hero"><div class="cendra-hero-content"><div class="cendra-badge">FINANCIAL INTELLIGENCE</div><div class="cendra-title">Cendra</div><div class="cendra-subtitle">Inteligencia financiera para negocios</div><div class="cendra-description">Convierte tus transacciones en indicadores, señales de riesgo y decisiones más claras.</div><div class="cendra-features"><span>Analítica financiera</span><span>Detección de riesgos</span><span>Score de salud</span></div></div><div class="cendra-hero-visual"><div class="hero-score-card"><span class="hero-score-label">MOTOR CENDRA</span><div class="hero-score-value">360°</div><span class="hero-score-status">Finanzas · Riesgos · Señales</span></div></div></div>
"""

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


def render_section_header(
    eyebrow: str,
    title: str,
    description: str,
) -> None:

    section_html = f"""
<div class="section-header"><div class="section-eyebrow">{eyebrow}</div><div class="section-title">{title}</div><div class="section-description">{description}</div></div>
"""

    st.markdown(
        section_html,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:

    st.info(
        "Sube un archivo Excel o CSV "
        "para comenzar el análisis financiero."
    )

    with st.expander(
        "¿Qué puede analizar Cendra?"
    ):

        st.markdown(
            """
            - Indicadores financieros y comerciales
            - Comparación contra períodos anteriores
            - Cendra Score de salud financiera
            - Riesgo de concentración
            - Señales automáticas del negocio
            - Detección estadística de anomalías
            - Reporte ejecutivo descargable
            """
        )