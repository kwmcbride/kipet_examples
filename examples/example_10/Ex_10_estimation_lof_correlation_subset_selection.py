"""Example 10: Wavelength subset selection using lack of fit

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
    k1 = r1.parameter('k1', value=2, bounds=(0.0, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.0, 2.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    # Use this function to replace the old filename set-up
    r1.add_data('D_frame', category='spectral', file='data/Dij.txt')

    rA = k1*A
    rB = k2*B
    
    # Define the reaction model
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    
    r1.bound_profile(var='S', bounds=(0, 200))

    # Settings
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 60
    # This needs to be set to False to keep the reduced hessian output surpressed
    r1.settings.parameter_estimator.tee = False
    r1.settings.parameter_estimator.covariance = 'ipopt_sens'
    r1.settings.solver.mu_init = 1e-4
    r1.settings.solver.linear_solver = 'ma57'
    
    r1.run_opt()
   
    # Display the results
    r1.results.show_parameters
        
    if with_plots:
        r1.plot()
    
    
    """Wavelength subset selection methods"""
    
    # # See the tutorial for more info: Tutorial 13
    lof = r1.lack_of_fit()
    correlations = r1.wavelength_correlation(corr_plot=True)
    
    r1.run_lof_analysis()
    
    # Follow the tutorial for this next step:
    # A specific range is selected and smaller steps are made
    r1.run_lof_analysis(step_size = 0.01, search_range = (0, 0.12))
    
    # It seems like this is a good cut-off point
    subset = r1.wavelength_subset_selection(n=0.095) 
    
    # Solve the ParameterEstimator using the wavelength subset
    subset_results = r1.run_opt_with_subset_lambdas(subset) 
    
    # # # Display the new results
    subset_results.show_parameters
