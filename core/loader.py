from pathlib import Path

import pandas as pd


def load_file(file) -> pd.DataFrame:
    extension = Path(file.name).suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(file)

    raise ValueError(f"Formato no soportado: {extension}")