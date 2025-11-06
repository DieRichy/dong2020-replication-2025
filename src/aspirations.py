# src/aspirations

### define the 4 different aspirations mentioned in the paper ###

import numpy as np
from src.config import GAMMA,W,MU

#Historical Aspirations 
class HistoricalAspiration:
    def __init__(self,init_val):
        self.value = init_val

    def update(self, performance): #update based on its historical performance
        self.value = GAMMA * self.value + (1 - GAMMA) * (1 + MU) * performance

class SocialAspiration:
    def __init__(self, init_val):
        self.value = init_val

    def update(self, ref_performance): #update based on its reference group P
        self.value = GAMMA * self.value + (1 - GAMMA) * (1 + MU) * ref_performance
        
class MixedAspiration:
    def __init__(self, init_val):
        self.value = init_val
 
    def update(self, performance, ref_performance):# update based on both its reference group P and historical performance
        self.value = GAMMA * self.value + (1 - GAMMA) * (1 + MU) * (W * performance + (1 - W) * ref_performance)

class SwitchingAspiration:
    def __init__(self, init_val):
        self.value = init_val
    
    def update(self,self_performance,ref_performance):#dynamically switching based on either its reference group P or historical performance
        performance = ref_performance if self_performance < ref_performance else self_performance
        self.value = GAMMA * self.value + (1 - GAMMA) * (1 + MU) * performance
