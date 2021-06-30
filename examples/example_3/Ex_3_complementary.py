"""
Example 3: Simulation example using complementary states

Note: When using functions such as exp, you need to import them from pyomo.core
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports
from pyomo.core import exp

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('reaction-1')
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1.0)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    T = r1.state('T', value=290, description='Temperature')
    V = r1.volume(value=100, description='Volume')

    # Model constants
    cA0 = r1.constant('ca0', value=4.0)
    v0 = r1.constant('v0', value=240)
    
    cpA = r1.constant('cpA', value=30)
    cpB = r1.constant('cpB', value=60)
    cpC = r1.constant('cpC', value=20)
    
    TA0 = r1.constant('TA0', value=305)
    hrxnA = r1.constant('hrxnA', value=6500)
    hrxnB = r1.constant('hrxnB', value=8000)
    Tc = r1.constant('Tc', value=298)
    Uc = r1.constant('Uc', value=35000)

    # Define the expressions
    k1 = r1.add_expression('k1', 1.25*exp((9500/1.987)*(1/320.0 - 1/T)))
    k2 = r1.add_expression('k2', 0.08*exp((7000/1.987)*(1/290.0 - 1/T)))
    
    rA = r1.add_reaction('rA', k1*A)
    rB = r1.add_reaction('rB', k2*B)
    
    SM = {
        'A': [ -1,  0],
        'B': [0.5, -1],
        'C': [  0,  3]
        }
    
    RE = r1.reactions_from_stoich(SM, add_odes=False)
    RE['A'] += cA0*v0/V
    r1.add_odes(RE)
    
    # Energy balances
    T1 = Uc*(Tc - T) # heat transfer
    T2 = cA0*v0*cpA*(T - TA0) # enthalpy from adding A
    T3 = V*(hrxnA*rA - hrxnB*rB) # heat of reaction
    Den = (cpA*A + cpB*B + cpC*C)*V + 3500.0 # heat capacities/density
    
    r1.add_ode('T', (T1 + T2 + T3)/Den )
    
    # ODE for volume
    r1.add_ode('V', v0 )
    
    # Simulation requires a time span
    r1.set_time(2.0)
    
    # This is difficult to simulate because it is really stiff
    # Change some of the default settings
    r1.settings.collocation.nfe = 120
    r1.settings.collocation.ncp = 1
    r1.settings.general.add_volume_terms = True
    #r1.settings.simulator.method = 'dae.collocation'

    # Simulation
    r1.simulate()  

    # Create plots
    if with_plots:
        r1.report()
