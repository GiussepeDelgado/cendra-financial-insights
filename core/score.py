import pandas as pd

from core.analytics import calculate_kpis


SCORE_WEIGHTS = {
    "profitability": 0.35,
    "growth": 0.25,
    "expense_control": 0.20,
    "stability": 0.20,
}


def clamp(
    value: float,
    minimum: float = 0,
    maximum: float = 100,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


def calculate_percentage_change(
    current_value: float,
    previous_value: float,
) -> float | None:

    if previous_value <= 0:
        return None

    return (
        (current_value - previous_value)
        / abs(previous_value)
        * 100
    )


def calculate_profitability_score(
    margin: float,
) -> float:

    # Escala heurística v0.1:
    # margen <= 0%  → 0
    # margen 10%    → 25
    # margen 20%    → 50
    # margen 30%    → 75
    # margen >= 40% → 100

    return clamp(
        margin * 2.5
    )


def calculate_growth_score(
    current_sales: float,
    previous_sales: float,
) -> float | None:

    growth = calculate_percentage_change(
        current_sales,
        previous_sales,
    )

    if growth is None:
        return None

    # -25% crecimiento → 0
    #   0% crecimiento → 50
    # +25% crecimiento → 100

    return clamp(
        50 + growth * 2
    )


def calculate_expense_control_score(
    current_expenses: float,
    previous_expenses: float,
) -> float | None:

    expense_growth = calculate_percentage_change(
        current_expenses,
        previous_expenses,
    )

    if expense_growth is None:
        return None

    # Gastos estables → 70
    # Gastos +30%    → 40
    # Gastos -20%    → 90

    return clamp(
        70 - expense_growth
    )


def calculate_stability_score(
    df: pd.DataFrame,
) -> float | None:

    sales = df[
        df["tipo"].str.lower() == "venta"
    ].copy()

    if sales.empty:
        return None

    monthly_sales = (
        sales
        .set_index("fecha")
        .resample("ME")["monto"]
        .sum()
    )

    # Evitamos evaluar estabilidad
    # con muy pocos meses.

    if len(monthly_sales) < 3:
        return None

    mean_sales = monthly_sales.mean()

    if mean_sales <= 0:
        return None

    std_sales = monthly_sales.std()

    coefficient_variation = (
        std_sales / mean_sales
    )

    return clamp(
        100
        - coefficient_variation * 100
    )


def calculate_weighted_score(
    dimensions: dict,
) -> float | None:

    available_dimensions = {
        key: value
        for key, value in dimensions.items()
        if value is not None
    }

    if not available_dimensions:
        return None

    available_weight = sum(
        SCORE_WEIGHTS[key]
        for key in available_dimensions
    )

    if available_weight <= 0:
        return None

    weighted_total = sum(
        value * SCORE_WEIGHTS[key]
        for key, value
        in available_dimensions.items()
    )

    return (
        weighted_total
        / available_weight
    )


def calculate_cendra_score(
    current_df: pd.DataFrame,
    previous_df: pd.DataFrame,
) -> dict:

    current = calculate_kpis(current_df)
    previous = calculate_kpis(previous_df)

    profitability_score = (
        calculate_profitability_score(
            current["margin"]
        )
    )

    growth_score = calculate_growth_score(
        current["sales"],
        previous["sales"],
    )

    expense_control_score = (
        calculate_expense_control_score(
            current["expenses"],
            previous["expenses"],
        )
    )

    stability_score = (
        calculate_stability_score(
            current_df
        )
    )

    dimensions = {
        "profitability": profitability_score,
        "growth": growth_score,
        "expense_control": expense_control_score,
        "stability": stability_score,
    }

    total_score = calculate_weighted_score(
        dimensions
    )

    available_count = sum(
        value is not None
        for value in dimensions.values()
    )

    coverage = (
        available_count
        / len(dimensions)
        * 100
    )

    return {
        "total": (
            round(total_score, 1)
            if total_score is not None
            else None
        ),
        "profitability": (
            round(profitability_score, 1)
            if profitability_score is not None
            else None
        ),
        "growth": (
            round(growth_score, 1)
            if growth_score is not None
            else None
        ),
        "expense_control": (
            round(expense_control_score, 1)
            if expense_control_score is not None
            else None
        ),
        "stability": (
            round(stability_score, 1)
            if stability_score is not None
            else None
        ),
        "coverage": round(coverage, 1),
    }


def classify_score(
    score: float | None,
) -> dict:

    if score is None:
        return {
            "status": "Sin datos suficientes",
            "level": "unknown",
            "message": (
                "No existe información suficiente "
                "para calcular la salud financiera."
            ),
        }

    if score >= 80:
        return {
            "status": "Excelente",
            "level": "excellent",
            "message": (
                "Los indicadores disponibles muestran "
                "una situación financiera sólida."
            ),
        }

    if score >= 65:
        return {
            "status": "Saludable",
            "level": "healthy",
            "message": (
                "Los indicadores disponibles muestran "
                "una situación financiera favorable."
            ),
        }

    if score >= 50:
        return {
            "status": "Atención",
            "level": "warning",
            "message": (
                "Existen áreas financieras "
                "que requieren seguimiento."
            ),
        }

    return {
        "status": "Riesgo",
        "level": "risk",
        "message": (
            "Se detectan señales financieras "
            "que requieren revisión."
        ),
    }