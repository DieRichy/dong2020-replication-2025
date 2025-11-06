# src/simulation.py
import numpy as np
import pandas as pd
from src.aspirations import *
from src.config import *

def compute_peer_perf(i, P, strategy="stepwise"):
    """Compute reference group performance for firm i based on chosen strategy."""
    n = len(P)
    if strategy == "conservative":
        return np.mean(P)
    elif strategy == "stepwise":
        num_ref = max(1, int(PERCENTILE_STEPWISE * n))
        diffs = np.abs(P - P[i])
        idx = np.argsort(diffs)[1:num_ref+1]
        return np.mean(P[idx])
    elif strategy == "ambitious":
        num_ref = max(1, int(PERCENTILE_STEPWISE * n))
        top_idx = np.argsort(P)[-num_ref:]
        return np.mean(P[top_idx])
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def run_single_simulation(aspiration_type, d, v, strategy="stepwise",
                          n_firms=NUM_ORG, n_periods=NUM_PERIOD):
    # ---- initialization ----
    T = np.random.randn(n_firms)
    M = np.random.randn(n_firms)
    P = T + M
    A0 = np.random.randn(n_firms)  # Initial aspirations

    # Initialize aspiration objects
    if aspiration_type == "historical":
        aspirations = [HistoricalAspiration(a) for a in A0]
    elif aspiration_type == "social":
        aspirations = [SocialAspiration(a) for a in A0]
    elif aspiration_type == "mixed":
        aspirations = [MixedAspiration(a) for a in A0]
    elif aspiration_type == "switching":
        aspirations = [SwitchingAspiration(a) for a in A0]
    else:
        raise ValueError("Unknown aspiration type")

    performance_records = []

    # ---- simulate over time ----
    for _ in range(n_periods):
        # Market update (independent of decision)
        new_M = v * M + (1 - v) * np.random.randn(n_firms)
        new_T = np.zeros(n_firms)

        # Technological choice decision (using current P_{t-1} vs A_{t-1})
        for i, asp in enumerate(aspirations):
            if P[i] < asp.value:
                S_it = np.random.randn()
                new_T[i] = max(d * T[i], S_it)
            else:
                new_T[i] = d * T[i]

        # Compute new performance P_t
        new_P = new_T + new_M

        # Aspiration update — MUST use new_P (P_t)
        for i, asp in enumerate(aspirations):
            peer_perf = compute_peer_perf(i, new_P, strategy)   #  use new_P !
            if aspiration_type == "historical":
                asp.update(new_P[i])
            elif aspiration_type == "social":
                asp.update(peer_perf)
            elif aspiration_type == "mixed":
                asp.update(new_P[i], peer_perf)
            else:
                asp.update(new_P[i], peer_perf)


        # Update states
        T, M, P = new_T, new_M, new_P
    
        performance_records.append(new_P.copy())

    return np.array(performance_records)


# experiment functions
def run_experiment(n_firms,n_periods,strategy,n_runs):
    records = []

    for (label, d, v) in UNCERTAINTY_LEVELS:
        tech_level = "Low" if "low_tech" in label else "High"
        market_level = "Low" if "low_market" in label else "High"

        for asp in ASPIRATION_TYPE:
            for run_id in range(n_runs):
                perf_matrix = run_single_simulation(
                    aspiration_type=asp, d=d, v=v,
                    strategy=strategy, n_firms=n_firms, n_periods=n_periods,
                )

                mean_perf = np.mean(perf_matrix, axis=0)
                risk = np.std(perf_matrix, axis=0)
                
                # 为每个组织创建记录
                for org_id, (org_perf, org_risk) in enumerate(zip(mean_perf, risk)):
                    records.append({
                        "Aspiration": asp,
                        "Tech_Uncert_Level": tech_level,
                        "Market_Uncert_Level": market_level,
                        "Strategy": strategy,
                        "Performance": org_perf,
                        "Risk": org_risk,
                        "Run_ID": run_id,
                        "Org_ID": org_id
                    })

    df = pd.DataFrame(records)
    print(f"\n📊 Raw data for ANOVA - Shape: {df.shape}")
    print(f"📈 Total observations: {len(df)}")
    return df