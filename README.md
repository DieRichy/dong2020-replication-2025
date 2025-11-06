# Replicating Dong (2020) — *Technological Choices under Uncertainty: Does Organizational Aspiration Matter?*

This repository replicates the simulation study from:

> **Dong, J. Q. (2020).** *Technological choices under uncertainty: Does organizational aspiration matter?*  
> *Strategic Management Journal*, 41(12), 1–19. [https://doi.org/10.1002/smj.3253]

The replication reproduces **Table 1** and related analyses by implementing the agent-based simulation model described in the paper.  
It allows users to explore how **different types of organizational aspirations** (historical, social, mixed, switching) perform under **technological and market uncertainty**.

---

## 📂 Project Structure
```
Replicating_dong2020/
│
├── src/
│   ├── simulation.py               # Core agent-based simulation logic
│   ├── aspirations.py              # Definitions for aspiration models (Historical, Social, Mixed, Switching)
│   ├── config.py                   # Experiment parameters (γ, μ, uncertainty levels, etc.)
│   ├── analysis.py                 # ANOVA and group mean difference computations (Table 1 reproduction)
│   ├── plotting.py                 # Visualization utilities for Table 1-style plots and dynamics
│
├── outputs/                        # Automatically generated plots and results
│   ├── aspiration_effects_diff.png
│   ├── dynamic_trends.png
│   ├── market_uncertainty_effects.png
│   ├── summary_table.csv
│   ├── table1_anova_heatmap.png
│   ├── table1_anova_style_summary.csv
│   ├── tech_uncertainty_effects.png
│
├── streamlit_ui.py                 # Optional interactive interface for running and visualizing results
│
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation (this file)
```
## 🚀 How to Run

### 1️⃣ Create environment
```bash
conda create -n replicating_dong2020 python=3.12
conda activate replicating_dong2020
pip install -r requirements.txt
```
⚠️ if you are using anaconda on Mac OS, "pip install -r requirements.txt" might be slient failure
you can simply try "conda install -c conda-forge numpy pandas seaborn statsmodels matplotlib streamlit -y"
### 2️⃣ Run simulations and analyses

From the project root:

```
bash
python src/simulation.py
```

This runs the agent-based simulations across all aspiration types and uncertainty levels
and saves raw results to `outputs/`.


### 3️⃣ Generate Anova summary

```bash
python src/analysis.py
```

This step:
*   Performs three-way ANOVA (Aspiration × Technological Uncertainty × Market Uncertainty)
*   Computes group mean differences from the overall mean, matching Dong (2020) Table 1
*   Outputs ANOVA table and group summaries to console

### 4️⃣ Plot results

```bash
python src/plotting.py
```

This generates and saves:
*   Bar plots of performance/risk differences
*   Heatmap of ANOVA F values
*   Dynamic performance trends
All figures are saved under `outputs/`.

### 5️⃣ (Optional) Run interactive dashboard

```bash
streamlit run streamlit_ui.py
```

This launches an interface where you can select aspiration type, uncertainty level, and view results interactively.
Also, it provides a more intuitive way to adjust aspiration update strategy：
(1️⃣"Stepwise",2️⃣"Ambitious" and 3️⃣"Conservative") 
---

## 📊 Output Overview
*   ANOVA summary (Performance and Risk)
*   Group mean differences (Performance & Risk relative to overall mean)
*   Visualization:
    *   Aspiration effects
    *   Technological & market uncertainty effects
    *   ANOVA heatmap
    *   Dynamic trends over runs

All outputs are saved in the `outputs/` folder.

---

## 🧠 Methodological Notes
*   Model follows agent-based simulation design from Dong (2020):
    *   200 organizations simulated over 1,000 periods
    *   Four aspiration types: historical, social, mixed, switching
    *   Two levels of technological uncertainty (d = 0.9 / 0.5)
    *   Two levels of market uncertainty (v = 0.9 / 0.5)
    *   Each simulation run generates mean performance and risk across organizations.
    *   ANOVA and group mean differences mirror Table 1 in the original article.

---

## 📚 Citation

If you use or build upon this replication, please cite:

Dong, J. Q. (2020). Technological choices under uncertainty: Does organizational aspiration matter?
Strategic Management Journal, 41(12), 1–19.
DOI: 10.1002/smj.3253

---

## 🧩 Author

Replication by Daizhi Fan, based on Dong (2020).
Contact: fandaizhi@outlook.com

---

## 🪪 License

This project is released under the MIT License.
You are free to reuse and modify the code with proper attribution.

---

## ✅ Example output preview

Example console output (excerpt):

📄 Table 1-style ANOVA (no Residuals):

| Metric      | Source                        | Sum Sq | df | F value | p-value |
|--------------|-------------------------------|--------|----|----------|---------|
| Performance  | C(Aspiration)                 | 38568  | 3  | 1.45e+04 | <0.001 |
| Risk         | C(Aspiration)                 | 3546   | 3  | 3.55e+03 | <0.001 |
| ... | ... | ... | ... | ... | ... |

📊 Group mean differences from overall mean:

| Aspiration | Perf_diff | Risk_diff |
|---|---|---|
| Historical | -0.347 | -0.013 |
| Social | 0.410 | 0.019 |
| Mixed | 0.251 | 0.002 |
| Switching | -0.314 | -0.008 |

