import pandas as pd


def normalize_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:

    data = df.copy()

    # =========================
    # COLUMNAS
    # =========================

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # =========================
    # FECHA
    # =========================

    if "fecha" in data.columns:
        data["fecha"] = pd.to_datetime(
            data["fecha"],
            errors="coerce",
        )

    # =========================
    # CAMPOS NUMÉRICOS
    # =========================

    numeric_columns = [
        "cantidad",
        "monto",
    ]

    for column in numeric_columns:

        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    # =========================
    # TEXTOS
    # =========================

    text_columns = [
        "tipo",
        "categoria",
        "producto",
        "cliente",
    ]

    for column in text_columns:

        if column in data.columns:

            data[column] = (
                data[column]
                .astype("string")
                .str.strip()
            )

    return data