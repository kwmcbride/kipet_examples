"""Example 15: Multiple Experimental Datasets and unwanted contributions with
 the new KipetModel
 
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
    
    lab = kipet.ReactionSet()
    
    r1 = lab.new_reaction(name='reaction-1')
    r1.settings.parameter_estimator.covariance = None
    
    # Add the parameters
    k1 = r1.parameter('k1', value=1.3, bounds=(0.0, 2.0))
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
    
    filename1 = 'data/Dij_multexp_tiv_G.txt'
    filename2 = 'data/Dij_multexp_tv_G.txt'
    filename3 = 'data/Dij_multexp_no_G.txt'
    
    # Model 1
    r1.add_data(category='spectral', file=filename1)
    r1.spectra.decrease_wavelengths(1)

    r1.unwanted_contribution('time_invariant_G')
    # Each model has it's own unwanted G settings for the parameter estimation
    r1.settings.solver.linear_solver = 'ma57'
    r1.settings.parameter_estimator.solver = 'ipopt'
    #r1.settings.parameter_estimator.scaled_variance = True
    r1.settings.parameter_estimator.tee = True
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 60
    
    # Model 2
    r2 = lab.new_reaction(name='reaction-2', model=r1)
    r2.add_data(category='spectral', file=filename2)
    r2.spectra.decrease_wavelengths(1)
    r2.unwanted_contribution('time_variant_G')
    
    # Model 3
    r3 = lab.new_reaction(name='reaction-3', model=r1)
    r3.add_data(category='spectral', file=filename3)
    r3.spectra.decrease_wavelengths(1)
    
    # Settings
    lab.settings.general.shared_spectra=True
    # Perform the parameter estimation
   
    lab.run_opt()
 
    # Plot the results
    if with_plots:
        lab.report()
