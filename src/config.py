# src/config.py
# #definition of all parameters

### Simulation Parameters ###

NUM_ORG = 200 # from Figure 1 in paper
NUM_REPEAT = 1000 # from Figure 1 in paper  # subject to change 
NUM_PERIOD = 1000 # from Figure 1 in paper


### Behavioral Parameters ###
GAMMA =  0.5
MU = 0.05 
W = 0.5 # from paper: "to balance the difference between historical and social components, I assumed an equal weight"

### reference group strategy ###
REFERENCE_STRATEGY = "stepwise"  # optional: "conservative", "stepwise", "ambitious"
PERCENTILE_STEPWISE = 0.1        # how many percent of the most similar peers


### Uncertainty ### 
"""
tech deterioration : d 
market turbulence : v 
"""
TECH_UNCERT_LOW = 0.9 # from paper 10% technology deterioration: d = 0.9
TECH_UNCERT_HIGH = 0.5 # from paper 50% technology deterioration: d = 0.5
MARKET_UNCERT_LOW = 0.9 # v = 0.9
MARKET_UNCERT_HIGH = 0.5 # v = 0.5


### Experiment Setup ###

ASPIRATION_TYPE = ["historical", "social", "mixed", "switching"]

"""the experiment is a :
4 (4 types of aspirations) * 2(low and high level of technological uncertainty) * 2 (low and high level of market turbulence)
"""
UNCERTAINTY_LEVELS = [
    ("low_tech_low_market",TECH_UNCERT_LOW,MARKET_UNCERT_LOW), 
    ("low_tech_high_market",TECH_UNCERT_LOW,MARKET_UNCERT_HIGH),
    ("high_tech_low_market",TECH_UNCERT_HIGH,MARKET_UNCERT_LOW),
    ("high_tech_high_market",TECH_UNCERT_HIGH,MARKET_UNCERT_HIGH)
]

#random seed
SEED = 7