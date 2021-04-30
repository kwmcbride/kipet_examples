"""Example 6: Estimation with non-absorbing species with new KipetModel"""

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
    k1 = r1.parameter('k1', value=1.5, bounds=(0.01, 4.0))
    k2 = r1.parameter('k2', value=0.33, bounds=(0.01, 2.0))
    
    # Declare the components and give the initial values
    # Perhaps use an Enum on components...
    A = r1.component('A', value=1)
    B = r1.component('B', value=0.0, known=True, bounds=(1e-8, 1e-4))
    C = r1.component('C', value=0.0, absorbing=False)
    
    # Use this function to replace the old filename set-up
    #r1.add_data(category='spectral', file='/home/kevin/Dev/kipet_examples/examples/example_6/data/Dij.txt')    
    
    file = '/home/kevin/Dev/kipet_examples/examples/example_6/data/non_abs.csv'
    full_data = kipet_model.read_data_file(file)
    r1.add_data(category='spectral', data=full_data)
    
    #% Try to make stoic matrix from given inputs
    
    rA = r1.add_reaction('rA', k1*A, description='Reaction A' )
    rB = r1.add_reaction('rB', k2*B, description='Reaction B' )
    
    r1.add_ode('A', -rA)
    r1.add_ode('B', rA - rB)
    r1.add_ode('C', rB)

    # Use the stoichiometry to build the reaction network:
    stoich_data = {'rA': [-1, 1, 0],
                   'rB': [0, -1, 1]}
    
    r1.build_from_reaction_matrix(stoich_data)
    
    # Settings
    r1.settings.collocation.ncp = 3
    r1.settings.collocation.nfe = 60
    r1.settings.variance_estimator.use_subset_lambdas = True
    r1.settings.variance_estimator.max_iter = 5
    r1.settings.variance_estimator.tolerance = 1e-4
    r1.settings.parameter_estimator.tee = False
    
    #r1.settings.general.initialize_pe = True
    #r1.settings.general.scale_pe = True
    r1.settings.parameter_estimator.sim_init = True
    
    r1.run_opt()
    
    # Display the results
    r1.results.show_parameters
    
    # New plotting methods
    if with_plots:
        r1.plot()