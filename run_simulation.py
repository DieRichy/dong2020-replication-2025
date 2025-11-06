# test_run.py
import numpy as np
import pandas as pd
from src.simulation import run_experiment
from src.analysis import create_table_detailed

def main():
    # 1. Quick view Experiment （aggregated data)
    print("🚀 Running aggregated simulation...")
    df_agg = run_experiment(
        n_firms=100, n_periods=200, n_runs=10,
        strategy="ambitious",
    )
    print(f"Aggregated data shape: {df_agg.shape}")
    
    # 2. Quick view Experiment （Anova)
    print("\n🚀 Running raw data simulation...")
    df_raw = run_experiment(
        n_firms=100, n_periods=200, n_runs=10, 
        strategy="ambitious",
    )
    print(f"Raw data shape: {df_raw.shape}")
    print(df_raw.head(10))
    # 3. run Anova
    print("\n🔬 Running ANOVA Analysis...")
    anova = create_table_detailed(df_raw)
    
    return df_agg,anova

if __name__ == "__main__":
    df_agg, df_raw = main()