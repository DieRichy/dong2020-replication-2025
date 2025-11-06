# test_run.py
import numpy as np
import pandas as pd
from src.simulation import run_experiment
from src.analysis import create_table_detailed

def main():
    # 1. Quick view Experiment （aggregated data)
    print("🚀 Running aggregated simulation...")
    df_agg = run_experiment(
        n_firms=NUM_ORG, n_periods=NUM_PERIOD, n_runs=NUM_REPEAT, # from config.py
        strategy="stepwise", #default,select from ["stepwise","ambitious","conservative"]
    )
    print(f"Aggregated data shape: {df_agg.shape}")
    
    # 2. Quick view Experiment （Anova)
    print("\n🚀 Running raw data simulation...")
    df_raw = run_experiment(
        n_firms=NUM_ORG, n_periods=NUM_PERIOD, n_runs=NUM_REPEAT, # from config.py
        strategy="stepwise", #default,select from ["stepwise","ambitious","conservative"]
    )
    print(f"Raw data shape: {df_raw.shape}")
    print(df_raw.head(10))
    # 3. run Anova
    print("\n🔬 Running ANOVA Analysis...")
    anova = create_table_detailed(df_raw)
    
    return df_agg,anova

if __name__ == "__main__":
    df_agg, df_raw = main()
