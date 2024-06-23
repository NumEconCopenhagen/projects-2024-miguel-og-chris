from scipy import optimize
import matplotlib.pyplot as plt

def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result

from scipy import optimize
import matplotlib.pyplot as plt

def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result



# Model Equations

from types import SimpleNamespace
import numpy as np

class MalthusEconomyBaseline:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 0.5
        par.eta = 0.5
        par.mu = 0.5
        par.X = 1
        par.A = 1
        par.L_0 = 2

    # Production function

    def output(self, L_t):
        return L_t**(1-self.par.alpha)*(self.par.A*self.par.X)**self.par.alpha

    # Output per capita

    def output_per_capita(self, L_t):
        return (self.par.A*self.par.X/L_t)**self.par.alpha

    # Birth rate:

    def birth_rate(self, L_t):
        return self.par.eta*(self.par.A*self.par.X/L_t)**self.par.alpha

    # Law of motion

    def L_t1(self, L_t):
        return self.par.eta*((self.par.A*self.par.X)**self.par.alpha)*L_t**(1-self.par.alpha)+(1-self.par.mu)*L_t

    # Population steady state

    def L_ss(self):
        return ((self.par.eta/self.par.mu)**(1/self.par.alpha))*self.par.A*self.par.X

    # output per capita steady state:

    def output_per_capita_ss(self):
        return self.par.mu/self.par.eta
    
    # Steady state solver


    def solve_ss(self):
        L_t = self.par.L_0
        population = [self.par.L_0]
        output_per_capita = [self.output_per_capita(self.par.L_0)]
        time = [0]

        while L_t != self.L_t1(L_t):
            L_next = self.L_t1(L_t)
            population.append(L_next)
            output_per_capita.append(self.output_per_capita(L_next))
            time.append(time[-1] + 1)
            L_t = L_next
            
        print("Periods passed before steady state is reached:", time[-1])
        print("Steady state population:", L_t)
        print("Steady state income per capita:", self.output_per_capita(L_t))

        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Population', color=color)
        ax1.plot(time, population, color=color, label='Population')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  
        color = 'tab:red'
        ax2.set_ylabel('Output per capita', color=color)  
        ax2.plot(time, output_per_capita, color=color, label='Output per capita')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  
        plt.title("Population and Output per Capita over Time")
        fig.legend(loc='center')
        plt.show()
        return

class MalthusEconomyBaselineParametrization:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 0.5
        par.mu = 0.2
        par.X = 1
        par.A = 1
        par.L_0 = 100

    # Production function

    def output(self, L_t,):
        return L_t**(1-self.par.alpha)*(self.par.A*self.par.X)**self.par.alpha

    # Output per capita

    def output_per_capita(self, L_t):
        return (self.par.A*self.par.X/L_t)**self.par.alpha

    # Birth rate:

    def birth_rate(self, L_t, eta):
        return eta*(self.par.A*self.par.X/L_t)**self.par.alpha

    # Law of motion

    def L_t1(self, L_t, eta):
        return eta*((self.par.A*self.par.X)**self.par.alpha)*L_t**(1-self.par.alpha)+(1-self.par.mu)*L_t

    # Population steady state

    def L_ss(self, eta):
        return ((eta/self.par.mu)**(1/self.par.alpha))*self.par.A*self.par.X

    # output per capita steady state:

    def output_per_capita_ss(self, eta):
        return self.par.mu/eta
    
    # Steady state solver


    def solve_ss(self, eta):
        L_t = self.par.L_0
        population = [self.par.L_0]
        output_per_capita = [self.output_per_capita(self.par.L_0)]
        time = [0]

        while L_t != self.L_t1(L_t, eta):
            L_next = self.L_t1(L_t, eta)
            population.append(L_next)
            output_per_capita.append(self.output_per_capita(L_next))
            time.append(time[-1] + 1)
            L_t = L_next

        return population, output_per_capita, time

    def plot_solutions(self):
        fig, ax1 = plt.subplots()

        # Set up the primary y-axis (Population)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Population', color='blue') 
        ax1.tick_params(axis='y', labelcolor='blue')

        # Set up the secondary y-axis (Output per capita)
        ax2 = ax1.twinx()
        ax2.tick_params(axis='y', labelcolor='red')

        # Loop through eta values and plot
        eta_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]  # Corrected range
        for eta in eta_values:
            time = self.solve_ss(eta)[2]
            population = self.solve_ss(eta)[0]
            ax1.plot(time, population, label=f'Population (eta={eta})', alpha=0.7)
            

        # Combine the legends from both y-axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.05, 0.5))

        fig.tight_layout()  
        plt.title("Population over Time")
        plt.show()


        # Plotting output per capita for different values of eta:

        fig, ax1 = plt.subplots()

        # Set up the primary y-axis (Population)
        ax1.set_xlabel('Time')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Set up the secondary y-axis (Output per capita)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Output per capita', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Loop through eta values and plot
        for eta in eta_values:
            time = self.solve_ss(eta)[2]
            output_per_capita = self.solve_ss(eta)[1]
            ax2.plot(time, output_per_capita, label=f'Output per capita (eta={eta})', alpha=0.7)
            

        # Combine the legends from both y-axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.05, 0.5))

        fig.tight_layout()  
        plt.title("Output per Capita over Time")
        plt.show()
        return   

class MalthusEconomyStochasticTechnology:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 0.5
        par.eta = 0.5
        par.mu = 0.5
        par.X = 1
        par.A_0 = 1
        par.A_mean = 0
        par.A_sigma = 0.002
        par.g_A = 0.02
        par.L_0 = 1

    # Production function

    def output(self, L_t):
        return L_t**(1-self.par.alpha)*(self.par.A*self.par.X)**self.par.alpha

    # Output per capita

    def output_per_capita(self, L_t, A_t):
        return (A_t*self.par.X/L_t)**self.par.alpha

    # Birth rate:

    def birth_rate(self, L_t, A_t):
        return self.par.eta*(A_t*self.par.X/L_t)**self.par.alpha

    # Law of motion

    def L_t1(self, L_t, A_t):
        return self.par.eta*((A_t*self.par.X)**self.par.alpha)*L_t**(1-self.par.alpha)+(1-self.par.mu)*L_t

    # Population steady state

    def L_ss(self, A_t):
        return ((self.par.eta/self.par.mu)**(1/self.par.alpha))*A_t*self.par.X

    # output per capita steady state:

    def output_per_capita_ss(self):
        return self.par.mu/self.par.eta
    
    def A_t1(self, A_t):
        return A_t*(1+self.par.g_A)+np.random.normal(self.par.A_mean, self.par.A_sigma)
    
    
    # Steady state solver


    def solve_ss(self):
        N = 200
        L_t = self.par.L_0
        A_t = self.par.A_0
        population = [self.par.L_0]
        output_per_capita = [self.output_per_capita(self.par.L_0, self.par.A_0)]
        time = [0]
        ss_time = []
        TFP = [self.par.A_0]

        for iterations in range(0,N,1):
            L_next = self.L_t1(L_t, A_t)
            A_next = self.A_t1(A_t)
            population.append(L_next)
            output_per_capita.append(self.output_per_capita(L_next, A_next))
            TFP.append(A_next)
            time.append(time[-1] + 1)
            L_t = L_next
            A_t = A_next
            
        print("Final income per capita:", self.output_per_capita(L_t, A_t))
        

        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Population', color=color)
        ax1.plot(time, population, color=color, label='Population')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  
        color = 'tab:red'
        ax2.set_ylabel('Output per capita', color=color)  
        ax2.plot(time, output_per_capita, color=color, label='Output per capita')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  
        plt.title("Population and Output per Capita over Time")
        fig.legend(loc='center')
        plt.show()

        return