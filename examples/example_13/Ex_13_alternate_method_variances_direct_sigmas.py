"""Example 13: Alternate method for variance estimation with new KipetModel

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

    # Add the parameters
    k1 = r1.parameter('k1', value=1.0, bounds=(0.01, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.001, 5.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1.0e-2)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
   
    # Define the reaction model
    r1.add_ode('A', -k1 * A )
    r1.add_ode('B', k1 * A - k2 * B )
    r1.add_ode('C', k2 * B )
    
    # Add data (after components)
    r1.add_data(category='spectral', file='data/varest.csv', remove_negatives=True)

    # Settings
    # r1.settings.general.no_user_scaling = True
    # r1.settings.variance_estimator.tolerance = 1e-10
    # r1.settings.parameter_estimator.tee = False
    
    # Additional settings for the alternate method with a range of device variances
    r1.settings.variance_estimator.method = 'direct_sigmas'
    r1.settings.variance_estimator.best_accuracy=1e-7
    r1.settings.variance_estimator.num_points=3
    # r1.settings.variance_estimator.initial_sigmas = 5e-6
    # r1.settings.variance_estimator.secant_point = 5e-5
    
    # You can access the method to calculate the variance with a fixed device variance directly
    #r1.settings.variance_estimator.fixed_device_variance = 1.3e-7
    
    # If you are using direct sigmas (multiple cases) run_opt will return a dict with variances
    var_dict = r1.run_opt()
    
    # New plotting methods
    if with_plots:
        r1.report()
        