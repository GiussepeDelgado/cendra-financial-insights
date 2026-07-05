import pandas as pd


def calculate_concentration_risk(
    df: pd.DataFrame,
) -> dict:

    sales = df[
        df["tipo"].str.lower() == "venta"
    ].copy()

    total_sales = sales["monto"].sum()

    if sales.empty or total_sales <= 0:
        return {
            "top_customer": "Sin datos",
            "customer_share": 0,
            "customer_level": "none",
            "top_product": "Sin datos",
            "product_share": 0,
            "product_level": "none",
        }

    # =========================
    # CONCENTRACIÓN POR CLIENTE
    # =========================

    customer_sales = (
        sales
        .groupby("cliente")["monto"]
        .sum()
        .sort_values(ascending=False)
    )

    top_customer = customer_sales.index[0]

    customer_share = (
        customer_sales.iloc[0]
        / total_sales
        * 100
    )

    # =========================
    # CONCENTRACIÓN POR PRODUCTO
    # =========================

    product_sales = (
        sales
        .groupby("producto")["monto"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_sales.index[0]

    product_share = (
        product_sales.iloc[0]
        / total_sales
        * 100
    )

    customer_hhi = calculate_hhi(
        customer_sales
    )

    product_hhi = calculate_hhi(
        product_sales
    )   

    return {
        "top_customer": top_customer,
        "customer_share": round(
            customer_share,
            1,
        ),
        "customer_level": classify_concentration(
            customer_share
        ),
        "top_product": top_product,
        "product_share": round(
            product_share,
            1,
        ),
        "product_level": classify_concentration(
            product_share
        ),
        "customer_hhi": customer_hhi,
        "product_hhi": product_hhi,
    }


def classify_concentration(
    share: float,
) -> str:

    if share >= 60:
        return "high"

    if share >= 40:
        return "medium"

    return "low"

def calculate_hhi(
    values: pd.Series,
) -> float:

    total = values.sum()

    if total <= 0:
        return 0

    shares = values / total

    hhi = (
        shares
        .pow(2)
        .sum()
        * 10000
    )

    return round(hhi, 0)