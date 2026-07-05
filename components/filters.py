from datetime import timedelta

import pandas as pd
import streamlit as st


def render_filters(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    st.sidebar.header("Filtros")

    # =========================
    # RANGO DE FECHAS
    # =========================

    min_date = df["fecha"].min().date()
    max_date = df["fecha"].max().date()

    date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # =========================
    # OPCIONES
    # =========================

    categories = sorted(
        df["categoria"]
        .dropna()
        .unique()
        .tolist()
    )

    products = sorted(
        df["producto"]
        .dropna()
        .unique()
        .tolist()
    )

    customers = sorted(
        df["cliente"]
        .dropna()
        .unique()
        .tolist()
    )

    # =========================
    # MULTISELECT
    # =========================

    selected_categories = st.sidebar.multiselect(
        "Categorías",
        options=categories,
    )

    selected_products = st.sidebar.multiselect(
        "Productos",
        options=products,
    )

    selected_customers = st.sidebar.multiselect(
        "Clientes",
        options=customers,
    )

    # =========================
    # DATAFRAME ACTUAL
    # =========================

    filtered_df = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_df = filtered_df[
            (
                filtered_df["fecha"].dt.date
                >= start_date
            )
            &
            (
                filtered_df["fecha"].dt.date
                <= end_date
            )
        ]

    else:
        start_date = min_date
        end_date = max_date

    # =========================
    # FILTROS COMERCIALES
    # =========================

    filtered_df = apply_commercial_filters(
        filtered_df,
        selected_categories,
        selected_products,
        selected_customers,
    )

    # =========================
    # PERÍODO ANTERIOR
    # =========================

    period_days = (
        end_date - start_date
    ).days + 1

    previous_end = (
        start_date - timedelta(days=1)
    )

    previous_start = (
        previous_end
        - timedelta(days=period_days - 1)
    )

    previous_df = df[
        (
            df["fecha"].dt.date
            >= previous_start
        )
        &
        (
            df["fecha"].dt.date
            <= previous_end
        )
    ]

    previous_df = apply_commercial_filters(
        previous_df,
        selected_categories,
        selected_products,
        selected_customers,
    )

    return filtered_df, previous_df


def apply_commercial_filters(
    df: pd.DataFrame,
    categories: list,
    products: list,
    customers: list,
) -> pd.DataFrame:

    result = df.copy()

    if categories:
        result = result[
            result["categoria"].isin(categories)
        ]

    if products:
        result = result[
            result["producto"].isin(products)
        ]

    if customers:
        result = result[
            result["cliente"].isin(customers)
        ]

    return result