"""Example 15: Time variant unwanted contributions with the new KipetModel
 
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports

# Kipet library imports
import kipet
                                                                                                    
if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('reaction-1')
    
    # Add the model parameters
    k1 = r1.parameter('k1', value=1.4, bounds=(0.0, 2.0))
    k2 = r1.parameter('k2', value=0.25, bounds=(0.0, 0.5))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1.0e-2)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    # define explicit system of ODEs
    rA = r1.add_reaction('rA', k1*A )
    rB = r1.add_reaction('rB', k2*B )
    
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )   
   
    # Add the data
    r1.add_data(category='spectral', file='data/Dij_tv_G.txt')
    
    # Settings
    r1.settings.collocation.nfe = 100
    
    r1.unwanted_contribution('time_variant_G')

    # Run KIPET
    r1.run_opt()

    if with_plots:
        r1.plot()
