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
    k1 = r1.parameter('k1', value=4.0, bounds=(0.0, 5.0))
    k2 = r1.parameter('k2', value=0.5, bounds=(0.0, 1.0))
    
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
    
    # Optinal bounds on the profiles
    #r1.bound_profile(var='S', comp='B', bounds=(0, 200))
    #r1.bound_profile(var='S', comp='A', bounds=(50, 65), profile_range=(1650, 1800))
    #r1.bound_profile(var='S', comp='C', bounds=(0, 300))
    #r1.bound_profile(var='C', comp='B', bounds=(0.0, 2.2e-4), profile_range=(0, 2))
    
    # Not currently working
    # r1.bound_point(var='S', comp='B', bounds=(210, 250), point=2000)
    # r1.bound_point(var='S', comp='C', bounds=(75, 75), point=1800)

    # Change some of the default settings
    r1.spectra.decrease_wavelengths(2)
    
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 50
    
    r1.settings.variance_estimator.fixed_device_variance = 3e-6
    
    # Perhaps remove the var_dict stuff from run_opt
    r1.run_opt()
    
    if with_plots:
        r1.report()
