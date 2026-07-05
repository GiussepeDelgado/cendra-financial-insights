import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    sales = df.loc[
        df["tipo"].str.lower() == "venta",
        "monto"
    ].sum()

    expenses = df.loc[
        df["tipo"].str.lower() == "gasto",
        "monto"
    ].sum()

    profit = sales - expenses

    margin = (
        profit / sales * 100
        if sales > 0
        else 0
    )

    return {
        "sales": sales,
        "expenses": expenses,
        "profit": profit,
        "margin": margin,
    }


def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    data["mes"] = (
        data["fecha"]
        .dt.to_period("M")
        .astype(str)
    )

    summary = (
        data
        .groupby(["mes", "tipo"])["monto"]
        .sum()
        .reset_index()
    )

    return summary


def get_sales_by_product(df: pd.DataFrame) -> pd.DataFrame:
    sales = df[
        df["tipo"].str.lower() == "venta"
    ]

    summary = (
        sales
        .groupby("producto")["monto"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return summary


def get_expenses_by_category(df: pd.DataFrame) -> pd.DataFrame:
    expenses = df[
        df["tipo"].str.lower() == "gasto"
    ]

    summary = (
        expenses
        .groupby("categoria")["monto"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return summary

def calculate_period_comparison(
    current_df: pd.DataFrame,
    previous_df: pd.DataFrame,
) -> dict:

    current = calculate_kpis(current_df)
    previous = calculate_kpis(previous_df)

    def percentage_change(
        current_value: float,
        previous_value: float,
    ) -> float | None:

        if previous_value == 0:
            return None

        return (
            (current_value - previous_value)
            / abs(previous_value)
            * 100
        )

    return {
        "sales": percentage_change(
            current["sales"],
            previous["sales"],
        ),
        "expenses": percentage_change(
            current["expenses"],
            previous["expenses"],
        ),
        "profit": percentage_change(
            current["profit"],
            previous["profit"],
        ),
        "margin": (
            current["margin"]
            - previous["margin"]
        ),
    }
def calculate_commercial_kpis(
    df: pd.DataFrame,
) -> dict:

    sales = df[
        df["tipo"].str.lower() == "venta"
    ]

    number_of_sales = len(sales)

    average_ticket = (
        sales["monto"].mean()
        if number_of_sales > 0
        else 0
    )

    if not sales.empty:
        product_sales = (
            sales
            .groupby("producto")["monto"]
            .sum()
        )

        customer_sales = (
            sales
            .groupby("cliente")["monto"]
            .sum()
        )

        top_product = product_sales.idxmax()
        top_customer = customer_sales.idxmax()

    else:
        top_product = "Sin datos"
        top_customer = "Sin datos"

    return {
        "average_ticket": average_ticket,
        "number_of_sales": number_of_sales,
        "top_product": top_product,
        "top_customer": top_customer,
    }