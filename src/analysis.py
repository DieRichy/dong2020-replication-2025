import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols


def create_table_detailed(df):
    """
    Produce a Table 1-like summary following Dong (2020):
    - Reports ANOVA results (without residuals)
    - Reports group mean differences from the overall mean for Performance & Risk
    """

    df = df.copy()
    df = df.dropna(subset=["Performance", "Risk"])
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    for col in ["Aspiration", "Tech_Uncert_Level", "Market_Uncert_Level"]:
        df[col] = df[col].astype("category")

    # --- ANOVA ---
    model_perf = ols(
        "Performance ~ C(Aspiration)*C(Tech_Uncert_Level)*C(Market_Uncert_Level)",
        data=df
    ).fit()
    anova_perf = sm.stats.anova_lm(model_perf, typ=2)
    anova_perf["Metric"] = "Performance"

    model_risk = ols(
        "Risk ~ C(Aspiration)*C(Tech_Uncert_Level)*C(Market_Uncert_Level)",
        data=df
    ).fit()
    anova_risk = sm.stats.anova_lm(model_risk, typ=2)
    anova_risk["Metric"] = "Risk"

    combined = (
        pd.concat([anova_perf, anova_risk])
        .reset_index()
        .rename(columns={
            "index": "Source",
            "sum_sq": "Sum Sq",
            "df": "df",
            "F": "F value",
            "PR(>F)": "p-value"
        })
    )

    # Drop Residual rows
    combined = combined[~combined["Source"].str.contains("Residual", na=False)]

    # Formatting
    combined["Sum Sq"] = combined["Sum Sq"].round(2)
    combined["F value"] = combined["F value"].round(2)
    combined["p-value"] = combined["p-value"].apply(lambda x: f"{x:.3g}")
    combined = combined[["Metric", "Source", "Sum Sq", "df", "F value", "p-value"]]

    print("\n📄 Table 1-style ANOVA (no Residuals):")
    print(combined)

    # --- Compute overall means for center-difference calculation ---
    overall_perf_mean = df["Performance"].mean()
    overall_risk_mean = df["Risk"].mean()

    print("\n📊 Group mean differences from overall mean:")

    # helper to compute group mean diff
    def summarize_diff(factor):
        summary = (
            df.groupby(factor)[["Performance", "Risk"]]
            .mean()
            .reset_index()
            .rename(columns={factor: "Level"})
        )
        summary["Perf_diff"] = summary["Performance"] - overall_perf_mean
        summary["Risk_diff"] = summary["Risk"] - overall_risk_mean
        summary = summary.round(3)
        print(f"\n→ {factor}")
        print(summary[["Level", "Perf_diff", "Risk_diff"]])
        return summary
    def summarize_diff_asp(factor):
        summary = (
            df.groupby(factor)[["Performance", "Risk"]]
            .mean()
            .reset_index()
            .rename(columns={factor: "Aspiration"})
        )
        summary["Perf_diff"] = summary["Performance"] - overall_perf_mean
        summary["Risk_diff"] = summary["Risk"] - overall_risk_mean
        summary = summary.round(3)
        print(f"\n→ {factor}")
        print(summary[["Aspiration", "Perf_diff", "Risk_diff"]])
        return summary

    asp_summary = summarize_diff_asp("Aspiration")
    tech_summary = summarize_diff("Tech_Uncert_Level")
    market_summary = summarize_diff("Market_Uncert_Level")

    return combined, asp_summary, tech_summary, market_summary