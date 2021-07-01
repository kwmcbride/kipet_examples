"""
Example 2: Simple example showing parameter fitting using spectral data
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=2.0, bounds=(0.01, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.01, 5.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1e-3)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    # Input data
    file_name = 'data/Dij.txt'
    r1.add_data(category='spectral', file=file_name)

    # Input the reactions as expressions
    rA = r1.add_reaction('rA', k1*A)
    rB = r1.add_reaction('rB', k2*B)
    
    # Input the ODEs
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    
    # Optinal bounds on the S profiles
    #r1.bound_profile(var='S', bounds=(0, 10))

    # Change some of the default settings
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 50
    
    r1.settings.variance_estimator.method='direct_sigmas'
    r1.settings.variance_estimator.best_accuracy=1.9219e-6
    r1.settings.variance_estimator.num_points=4
    
    # Perhaps remove the var_dict stuff from run_opt
    var_dict = r1.run_opt()
