"""
Example 6: Estimation with non-absorbing species
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
    k1 = r1.parameter('k1', value=1.5, bounds=(0.01, 4.0))
    k2 = r1.parameter('k2', value=0.33, bounds=(0.01, 2.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1)
    B = r1.component('B', value=0.0, known=True, bounds=(1e-8, 1e-4))
    C = r1.component('C', value=0.0, absorbing=False)
    
    # Add the data
    r1.add_data(category='spectral', file='data/Dij.txt')
    r1.spectra.decrease_wavelengths(4)
    r1.spectra.decrease_times(4)
    
    # Declare the reactions
    rA = r1.add_reaction('rA', k1*A, description='Reaction A' )
    rB = r1.add_reaction('rB', k2*B, description='Reaction B' )

    # Use the stoichiometry to build the reaction network:
    stoich_data = {'rA': [-1, 1, 0],
                   'rB': [ 0,-1, 1]}
    
    # Build ODEs from stoichiometry and add to the ReactionModel
    r1.reactions_from_stoich(stoich_data, add_odes=True)
    
    # Settings
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 60
    r1.settings.variance_estimator.max_iter = 5
    r1.settings.variance_estimator.tolerance = 1e-4
    r1.settings.parameter_estimator.tee = False
    
    #r1.settings.parameter_estimator.covariance = 'ipopt_sens'
    r1.settings.parameter_estimator.covariance = 'k_aug'
    
    # Perform parameter fitting
    r1.run_opt()
    
    # Display the results
    r1.results.show_parameters
    
    # Create plots
    if with_plots:
        r1.report()
        