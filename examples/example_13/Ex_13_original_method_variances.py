"""Example 13: Original method for variance estimation with new KipetModel

"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports

# Kipet library imports
from kipet import KipetModel

if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2:
        if int(sys.argv[1]):
            with_plots = False
 
    kipet_model = KipetModel()
    
    r1 = kipet_model.new_reaction('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=1.2, bounds=(0.01, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.001, 5.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', state='concentration', value=1e-3)
    B = r1.component('B', state='concentration', value=0.0)
    C = r1.component('C', state='concentration', value=0.0)
    
    r1.add_data(category='spectral', file='data/varest2.csv', remove_negatives=True)

    rates = {}
    rates['A'] = -k1 * A
    rates['B'] = k1 * A - k2 * B
    rates['C'] = k2 * B
    
    r1.add_odes(rates)

    # Settings
    r1.settings.general.no_user_scaling = True
    r1.settings.variance_estimator.tolerance = 1e-10
    r1.settings.parameter_estimator.tee = False
    r1.settings.parameter_estimator.solver = 'ipopt_sens'
    
    # This is all you need to run KIPET!
    r1.run_opt()
    
    # Display the results
    r1.results.show_parameters
    
    # New plotting methods
    if with_plots:
        r1.plot()

