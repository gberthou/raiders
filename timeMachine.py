import constants as cst
import math

class TimeMachine:
    def __init__(self):
        self.t = 0

    def update(self, dt):
        self.t += dt
        self.t %= cst.DAY_DURATION

    def getLuminance(self):
        #return cst.DAY_A * ((self.t - cst.DAY_DURATION/2)**2) + cst.DAY_LUM_MAX
        return (cst.DAY_LUM_MAX-cst.DAY_LUM_MIN)*(math.cos(self.t*2*math.pi/cst.DAY_DURATION + math.pi) + 1) / 2 + cst.DAY_LUM_MIN
        
