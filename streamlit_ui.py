# ui.py
import streamlit as st
import pandas as pd
import pathlib
from src.simulation import run_experiment
from src.analysis import create_table_detailed
from src.plotting import plot_results, out_dir


# --- Streamlit page config ---
st.set_page_config(page_title="Dong (2020) Simulation UI", layout="centered")

# --- Page header ---
st.title("Technological Choices under Uncertainty (Dong, 2020)")
st.caption("Replication of Table 1 — ANOVA results and performance/risk patterns")

# --- Sidebar configuration ---
st.sidebar.header("⚙️ Simulation Parameters")

num_org = st.sidebar.slider("Number of organizations", 50, 500, 200, step=50)
num_period = st.sidebar.slider("Number of periods", 100, 2000, 1000, step=100)
num_repeat = st.sidebar.slider("Number of repetitions", 10, 1000, 100, step=10)

# --- Strategy selection ---
strategy_label = st.sidebar.selectbox(
    "Reference group strategy (corresponds to Table 1 column)",
    ["stepwise (main model)", "conservative", "ambitious"]
)
strategy_map = {
    "stepwise (main model)": "stepwise",
    "conservative": "conservative",
    "ambitious": "ambitious"
}
strategy_choice = strategy_map[strategy_label]

st.sidebar.markdown("---")
st.sidebar.info("Adjust parameters, then click **Run Simulation** below to begin.")

# --- Run Simulation Button ---
if st.button("🚀 Run Simulation"):
    with st.spinner(f"Running simulation with strategy = '{strategy_choice}' ... please wait ⏳"):
 
        # === 3️⃣ Perform Table 1-like ANOVA ===
        df_raw =run_experiment(
            n_firms=num_org,
            n_periods=num_period,
            n_runs=num_repeat,
            strategy=strategy_choice,
        )
        table_anova = create_table_detailed(df_raw)

    st.success(f"✅ Simulation complete! Strategy used: **{strategy_choice}**")

    # --- Results display ---
    import pandas as pd
    
    if table_anova is not None:
        # unpack the tuple
        anova_df, aspiration_df, tech_uncert_df, market_uncert_df = table_anova
        st.subheader("📈 Anova Analytsis")
        st.dataframe(anova_df, hide_index=True, use_container_width=True)
        st.subheader("📈 Performance and Risk ~ 4 types of aspirations")
        st.dataframe(aspiration_df, hide_index=True, use_container_width=True)
        st.subheader("📈 Performance and Risk ~ Tech Uncertainty Level")
        st.dataframe(tech_uncert_df, hide_index=True, use_container_width=True)
        st.subheader("📈 Performance and Risk ~ Market Uncertainty Level")
        st.dataframe(market_uncert_df, hide_index=True, use_container_width=True)
            # --- Plot outputs ---
        plot_results(
        df_raw,
        anova_df=anova_df,
        asp_summary=aspiration_df,
        tech_summary=tech_uncert_df,
        market_summary=market_uncert_df)
        
        import pathlib
        output_dir = pathlib.Path(out_dir)

        st.markdown("---")
        st.subheader("📊 Visualization Results")

        # 1️⃣ Table 1 – ANOVA heatmap
        anova_img = output_dir / "table1_anova_heatmap.png"
        if anova_img.exists():
            st.markdown("### 📄 Table 1 – ANOVA Summary (F values heatmap)")
            st.image(anova_img, use_container_width=True)
        else:
            st.info("No Table 1 ANOVA heatmap found.")

        # 2️⃣ Aspiration effects
        asp_img = output_dir / "aspiration_effects_diff.png"
        if asp_img.exists():
            st.markdown("### 🧭 Aspiration Type Effects on Performance and Risk")
            st.image(asp_img, use_container_width=True)
        else:
            st.info("No aspiration effect plot found.")

        # 3️⃣ Technological and Market uncertainty effects
        tech_img = output_dir / "tech_uncertainty_effects.png"
        market_img = output_dir / "market_uncertainty_effects.png"

        if tech_img.exists() or market_img.exists():
            st.markdown("### ⚙️ Uncertainty Effects on Performance and Risk")
            cols = st.columns(2)
            if tech_img.exists():
                with cols[0]:
                    st.image(tech_img, caption="Technological Uncertainty", use_container_width=True)
            if market_img.exists():
                with cols[1]:
                    st.image(market_img, caption="Market Uncertainty", use_container_width=True)
        else:
            st.info("No uncertainty plots found.")

        # 4️⃣ Dynamic trends
        trend_img = output_dir / "dynamic_trends.png"
        if trend_img.exists():
            st.markdown("### 🔄 Dynamic Trends (Performance & Risk over Simulation Runs)")
            st.image(trend_img, use_container_width=True)
        else:
            st.info("No dynamic trend plot found.")

        st.markdown("---")
        st.success(f"✅ All plots generated for strategy **{strategy_choice}** are shown above.")
    else:
        st.info("No ANOVA results available.")

    