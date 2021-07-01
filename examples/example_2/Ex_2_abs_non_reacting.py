"""
Example 2: Simple example showing parameter fitting using spectral data
with a non-reacting solvent present
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports
import numpy as np

# Kipet library imports
import kipet


def Lorentzian_parameters():
    params_d = dict()
    params_d['alphas'] = [0.0,20]
    params_d['betas'] = [1600.0,2200.0]
    params_d['gammas'] = [30000.0,1000.0]
    return {'D':params_d}

if __name__ == "__main__":    

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    # First we generate the new absorbance of specie D
    wl_span = np.arange(1610, 2601, 10)
    S_parameters = Lorentzian_parameters()
    
    from kipet.calculation_tools.prob_gen_tools import generate_absorbance_data
    S_frame = generate_absorbance_data(wl_span,S_parameters) 
    kipet.write_data('data/Sij2.txt', S_frame)
    
    r1 = kipet.ReactionModel('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=2.0, bounds=(0.01, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.01, 5.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1e-3)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    D = r1.component('D', value=1e-3, S=S_frame)
    
    # Input data
    file_name = 'data/Dij.txt'
    r1.add_data(category='spectral', file=file_name)

    r1.spectra.savitzky_golay(window=11)

    # Input the reactions as expressions
    rA = r1.add_reaction('rA', k1*A)
    rB = r1.add_reaction('rB', k2*B)
    
    # Input the ODEs
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    r1.add_ode('D', 0)
    
    # Optinal bounds on the S profiles
    #r1.bound_profile(var='S', bounds=(0, 10))

    # Change some of the default settings
    # r1.settings.variance_estimator.method = 'alternate'
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 60
    
    r1.settings.parameter_estimator.covariance = 'ipopt_sens'
    
    # Solve the model
    r1.run_opt()
    
    # Create plots
    if with_plots:
        r1.report()
    