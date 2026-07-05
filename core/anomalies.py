import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    threshold: float = 2.5,
) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    # Solo registros con monto válido
    data = data[
        data["monto"].notna()
    ].copy()

    if len(data) < 5:
        return pd.DataFrame()

    # =========================
    # DETECCIÓN POR TIPO
    # =========================

    anomaly_frames = []

    for transaction_type, group in data.groupby(
        data["tipo"].str.lower()
    ):

        if len(group) < 5:
            continue

        mean_amount = group["monto"].mean()
        std_amount = group["monto"].std()

        if (
            pd.isna(std_amount)
            or std_amount == 0
        ):
            continue

        current_group = group.copy()

        current_group["z_score"] = (
            (
                current_group["monto"]
                - mean_amount
            )
            / std_amount
        )

        current_group["es_anomalia"] = (
            current_group["z_score"].abs()
            >= threshold
        )

        current_group = current_group[
            current_group["es_anomalia"]
        ]

        if not current_group.empty:
            anomaly_frames.append(
                current_group
            )

    if not anomaly_frames:
        return pd.DataFrame()

    anomalies = pd.concat(
        anomaly_frames,
        ignore_index=True,
    )

    anomalies["desviacion"] = (
        anomalies["z_score"].abs()
    )

    anomalies = anomalies.sort_values(
        by="desviacion",
        ascending=False,
    )

    return anomalies