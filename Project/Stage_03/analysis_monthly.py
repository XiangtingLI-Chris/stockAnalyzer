from __future__ import annotations
import pandas as pd

def add_date_parts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add year / month / year_month columns.
    """
    df = df.copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
    df = df.dropna(subset=["trade_date"])

    df["year"] = df["trade_date"].dt.year.astype("int64")
    df["month"] = df["trade_date"].dt.month.astype("int64")
    df["year_month"] = df["trade_date"].dt.to_period("M").astype(str)

    return df

def monthly_up_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analysis: number of increase count for every stock in every `year_month`.
    Return columns: code, name, year, month, year_month, up_count
    """
    df2 = add_date_parts(df)

    grouped = (
        df2.groupby(["code", "name", "year", "month", "year_month"], dropna=False)
        .size()
        .reset_index(name="up_count")
    )

    grouped = grouped.sort_values(["code", "year", "month"]).reset_index(drop=True)
    return grouped

def common_months_across_years(monthly_df: pd.DataFrame, years: int = 3) -> pd.DataFrame:
    """
    Find: in the same month, stocks that have at least one increase record in `years` time range.
    :return: All records that satisfies the condition, columns: code, name, year_month, month, year, up_count.

    Explanation:
    - First list (code, month) appears in which years
    - Only keep those (code, month) whose appeared years >= `years`
    - Then go back to `monthly_df` and output `up_count` of every `year_month`
    """
    if monthly_df.empty:
        return monthly_df.copy()

    # count the amount of time that (code, month) appears in total
    year_coverage = (
        monthly_df.groupby(["code", "name", "month"])["year"]
        .nunique()
        .reset_index(name="year_cnt")
    )

    winners = year_coverage[year_coverage["year_cnt"] >= years][["code", "month"]]

    # go back to records of every `year_month`
    result = monthly_df.merge(winners, on=["code", "month"], how="inner")

    # clearer column order
    result = result[["code", "name", "year", "month", "year_month", "up_count"]].copy()
    result = result.sort_values(["code", "month", "year"]).reset_index(drop=True)
    return result