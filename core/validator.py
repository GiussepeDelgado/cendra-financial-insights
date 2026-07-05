import pandas as pd


REQUIRED_COLUMNS = {
    "fecha",
    "tipo",
    "categoria",
    "producto",
    "cliente",
    "cantidad",
    "monto",
}

VALID_TRANSACTION_TYPES = {
    "venta",
    "gasto",
}


def validate_dataframe(
    df: pd.DataFrame,
) -> dict:

    errors = []
    warnings = []

    # =========================
    # DATAFRAME VACÍO
    # =========================

    if df.empty:
        errors.append(
            "El archivo no contiene registros."
        )

        return {
            "errors": errors,
            "warnings": warnings,
        }

    # =========================
    # COLUMNAS OBLIGATORIAS
    # =========================

    missing_columns = (
        REQUIRED_COLUMNS - set(df.columns)
    )

    if missing_columns:
        columns = ", ".join(
            sorted(missing_columns)
        )

        errors.append(
            f"Faltan columnas obligatorias: "
            f"{columns}"
        )

        return {
            "errors": errors,
            "warnings": warnings,
        }

    # =========================
    # FECHAS INVÁLIDAS
    # =========================

    invalid_dates = df["fecha"].isna().sum()

    if invalid_dates > 0:
        errors.append(
            f"Se encontraron {invalid_dates} "
            f"fechas inválidas."
        )

    # =========================
    # MONTOS INVÁLIDOS
    # =========================

    invalid_amounts = df["monto"].isna().sum()

    if invalid_amounts > 0:
        errors.append(
            f"Se encontraron {invalid_amounts} "
            f"montos inválidos."
        )

    # =========================
    # MONTOS NEGATIVOS
    # =========================

    negative_amounts = (
        df["monto"] < 0
    ).sum()

    print(negative_amounts)

    if negative_amounts > 0:
        errors.append(
            f"Se encontraron {negative_amounts} "
            f"montos negativos."
        )

    # =========================
    # CANTIDADES INVÁLIDAS
    # =========================

    invalid_quantities = (
        df["cantidad"].isna()
    ).sum()

    if invalid_quantities > 0:
        errors.append(
            f"Se encontraron "
            f"{invalid_quantities} "
            f"cantidades inválidas."
        )

    # =========================
    # CANTIDADES NEGATIVAS
    # =========================

    negative_quantities = (
        df["cantidad"] < 0
    ).sum()

    if negative_quantities > 0:
        errors.append(
            f"Se encontraron "
            f"{negative_quantities} "
            f"cantidades negativas."
        )

    # =========================
    # TIPOS DESCONOCIDOS
    # =========================

    transaction_types = set(
        df["tipo"]
        .dropna()
        .str.lower()
        .unique()
    )

    invalid_types = (
        transaction_types
        - VALID_TRANSACTION_TYPES
    )

    if invalid_types:
        types = ", ".join(
            sorted(invalid_types)
        )

        errors.append(
            f"Tipos de transacción "
            f"no reconocidos: {types}."
        )

    # =========================
    # TEXTOS VACÍOS
    # =========================

    text_columns = [
        "categoria",
        "producto",
        "cliente",
    ]

    for column in text_columns:

        empty_values = (
            df[column].isna()
            |
            df[column]
            .astype("string")
            .str.strip()
            .eq("")
        ).sum()

        if empty_values > 0:
            warnings.append(
                f"La columna '{column}' "
                f"contiene {empty_values} "
                f"valores vacíos."
            )

    # =========================
    # DUPLICADOS
    # =========================

    duplicated_rows = (
        df.duplicated().sum()
    )

    if duplicated_rows > 0:
        warnings.append(
            f"Se detectaron "
            f"{duplicated_rows} "
            f"filas duplicadas."
        )

    # =========================
    # RESULTADO
    # =========================

    return {
        "errors": errors,
        "warnings": warnings,
    }