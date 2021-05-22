"""Example 1: Simple simulation example"""

# Standard library imports
import sys

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    # Create the ReactionModel instance
    r1 = kipet.ReactionModel('reaction-1')
    
    # Change the desired time basis here (if different from default)
    r1.unit_base.time = 's'

    # Add the model parameters
    k1 = r1.parameter('k1', value=2, units='1/s')
    k2 = r1.parameter('k2', value=0.2, units='1/s')
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1.0, units='M')
    B = r1.component('B', value=0.0, units='M')
    C = r1.component('C', value=0.0, units='M')
    
    # Input the reactions as expressions
    rA = r1.add_reaction('rA', k1*A)
    rB = r1.add_reaction('rB', k2*B)
    
    # Input the ODEs
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )

    # # Option to check the units of your models
    r1.check_model_units(display=True)
    
    # # Add dosing points 
    r1.add_dosing_point('A', 3, 0.3)
    
    # Simulations require a time span
    r1.set_time(10)
    
    # Change some of the default settings
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 50

    # Simulate
    r1.simulate()
    
    # Create plots
    if with_plots:
        r1.plot()
