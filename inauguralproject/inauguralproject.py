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
        par.w2A = 0.3

    def utility_A(self,x1A,x2A):
        return x1A**self.par.alpha * x2A**(1-self.par.alpha)

    def utility_B(self,x1B,x2B):
        return x1B**self.par.beta * x2B**(1-self.par.beta)

    def demand_A(self,p1):
        I = p1 * self.par.w1A + self.par.w2A
        return [self.par.alpha * I / p1, (1-self.par.alpha) * I]

    def demand_B(self,p1):
        return [self.par.beta * I / p1, (1-self.par.beta) * I]

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A) #Excess demand of good 1.
        eps2 = x2A-par.w2A + x2B-(1-par.w2A) #Excess demand of good 2.

        return eps1,eps2
    

# Edgeworth boks
def draw_edgeworth:
    model = ExchangeEconomyClass()
    par = model.par

# a. total endowment
    w1bar = 1.0
    w2bar = 1.0

# b. figure set up
    fig = plt.figure(frameon=False,figsize=(6,6), dpi=100)
    ax_A = fig.add_subplot(1, 1, 1)

    ax_A.set_xlabel("$x_1^A$")
    ax_A.set_ylabel("$x_2^A$")

    temp = ax_A.twinx()
    temp.set_ylabel("$x_2^B$")
    ax_B = temp.twiny()
    ax_B.set_xlabel("$x_1^B$")
    ax_B.invert_xaxis()
    ax_B.invert_yaxis()

# A
    ax_A.scatter(par.w1A,par.w2A,marker='s',color='black',label='endowment')

# limits
    ax_A.plot([0,w1bar],[0,0],lw=2,color='black')
    ax_A.plot([0,w1bar],[w2bar,w2bar],lw=2,color='black')
    ax_A.plot([0,0],[0,w2bar],lw=2,color='black')
    ax_A.plot([w1bar,w1bar],[0,w2bar],lw=2,color='black')

    ax_A.set_xlim([-0.1, w1bar + 0.1])
    ax_A.set_ylim([-0.1, w2bar + 0.1])    
    ax_B.set_xlim([w1bar + 0.1, -0.1])
    ax_B.set_ylim([w2bar + 0.1, -0.1])

    ax_A.legend(frameon=True,loc='upper right',bbox_to_anchor=(1.6,1.0));

N = 1000
x1_vec = np.linspace(0,1,N)

for