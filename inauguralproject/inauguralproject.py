def square(x):
    """ square numpy array
    
    Args:
    
        x (ndarray): input array
        
    Returns:
    
        y (ndarray): output array
    
    """
    
    y = x**2
    return y


# Definition of EchangeEconomyClass

from types import SimpleNamespace
import numpy as np

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w1B = 0.2
        par.w2A = 0.3
        par.w2B = 0.7

    def utility_A(self,x1A,x2A):
        return x1A**self.par.alpha * x2A**(1-self.par.alpha)

    def utility_B(self,x1B,x2B):
        return x1B**self.par.beta * x2B**(1-self.par.beta)

    def demand_A(self,p1):
        I = p1 * self.par.w1A + self.par.w2A
        return [self.par.alpha * I / p1, (1-self.par.alpha) * I]

    def demand_B(self,p1):
        I = p1 * self.par.w1B + self.par.w2B
        return [self.par.beta * I / p1, (1-self.par.beta) * I]
    
    # Demand functions functions with endowments as inputs

    def demand_A_endowment(self, w1A, w2A, p1):
        I = p1 * w1A + w2A
        return [self.par.alpha * I / p1, (1-self.par.alpha) * I]

    def demand_B_endowment(self, w1B, w2B, p1):
        I = p1 * w1B + w2B
        return [self.par.beta * I / p1, (1-self.par.beta) * I]

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A) #Excess demand of good 1.
        eps2 = x2A-par.w2A + x2B-(1-par.w2A) #Excess demand of good 2.

        return eps1,eps2
    
    # Check market clearing with endowments as inputs
    def check_market_clearing_endowment(self, w1A, w2A, w1B, w2B, p1):

        par = self.par

        x1A,x2A = self.demand_A_endowment(w1A, w2A, p1)
        x1B,x2B = self.demand_B_endowment(w1B, w2B, p1)

        eps1 = x1A-w1A + x1B-(1-w1A) #Excess demand of good 1.
        eps2 = x2A-w2A + x2B-(1-w2A) #Excess demand of good 2.

        return eps1,eps2
    