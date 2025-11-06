"""
plotting.py – Visualization utilities for Dong (2020) SMJ replication.
Generates Table 1-style plots, factor summaries, and dynamic trends.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Output directory
out_dir = Path(__file__).resolve().parents[1] / "outputs"
out_dir.mkdir(exist_ok=True)

sns.set(style="whitegrid", font_scale=1.1)


# ---------- Basic Plot Utilities ----------
def save_and_close(fig, name):
    """Helper to save figure and close."""
    path = out_dir / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Saved {name}.png")


# ---------- Aspiration Effects ----------
def plot_aspiration_effects(asp_summary):
    """Group mean differences (Perf_diff / Risk_diff) by Aspiration type."""
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    metrics = [("Perf_diff", "Blues_d"), ("Risk_diff", "Reds_d")]

    for i, (metric, palette) in enumerate(metrics):
        sns.barplot(data=asp_summary, x="Aspiration", y=metric, palette=palette, ax=ax[i])
        ax[i].axhline(0, color="gray", linestyle="--")
        ax[i].set_title(f"Group Mean Difference ({metric.replace('_diff','')}) by Aspiration Type")
        ax[i].set_xlabel("Aspiration Type")
        ax[i].set_ylabel("Group Mean Difference")

    plt.tight_layout()
    save_and_close(fig, "aspiration_effects_diff")


# ---------- Uncertainty Effects ----------
def plot_uncertainty_effects(tech_summary, market_summary):
    """Performance & Risk under Technological and Market Uncertainty."""
    for factor, df_summary in {
        "tech_uncertainty_effects": tech_summary,
        "market_uncertainty_effects": market_summary,
    }.items():
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        for i, (metric, palette) in enumerate([("Perf_diff", "Blues"), ("Risk_diff", "Reds")]):
            sns.barplot(data=df_summary, x="Level", y=metric, palette=palette, ax=ax[i])
            ax[i].axhline(0, color="gray", linestyle="--")
            ax[i].set_ylabel("Group Mean Difference")
            ax[i].set_title(f"{metric.replace('_diff','')} Difference by {factor.split('_')[0].capitalize()} Uncertainty")
        plt.tight_layout()
        save_and_close(fig, factor)


# ---------- ANOVA Heatmap ----------
def plot_table1_heatmap(anova_df):
    """Visualize ANOVA F values as heatmap."""
    df = anova_df[~anova_df["Source"].str.contains("Residual", na=False)]
    pivot = df.pivot(index="Source", columns="Metric", values="F value")
    plt.figure(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "F value"})
    plt.title("Table 1-style ANOVA Summary (F values)")
    plt.tight_layout()
    save_and_close(plt.gcf(), "table1_anova_heatmap")


# ---------- Dynamic Trends ----------
def plot_dynamic_trends(df):
    """Performance & Risk dynamics across simulation runs."""
    trend_df = (df.groupby(["Run_ID", "Aspiration"])[["Performance", "Risk"]]
                  .mean()
                  .reset_index())

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    for i, metric in enumerate(["Performance", "Risk"]):
        sns.lineplot(data=trend_df, x="Run_ID", y=metric, hue="Aspiration", marker="o", ax=ax[i])
        ax[i].set_title(f"{metric} Dynamics across Simulation Runs")
        ax[i].set_xlabel("Simulation Run")
        ax[i].set_ylabel(f"Mean {metric}")

    plt.tight_layout()
    save_and_close(fig, "dynamic_trends")


# ---------- Main Interface ----------
def plot_results(df, anova_df=None, asp_summary=None,
                 tech_summary=None, market_summary=None):
    """Generate all relevant figures."""
    if asp_summary is not None:
        plot_aspiration_effects(asp_summary)
    if tech_summary is not None and market_summary is not None:
        plot_uncertainty_effects(tech_summary, market_summary)
    if anova_df is not None:
        plot_table1_heatmap(anova_df)

    # Optional dynamic trend
    if "Run_ID" in df.columns:
        plot_dynamic_trends(df)

    print(f"📁 All plots saved to {out_dir.resolve()}")