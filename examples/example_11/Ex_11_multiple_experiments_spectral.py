"""
Example 11: Multiple Experimental Datasets with the new KipetModel
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
    
    # Define the general model
    lab = kipet.ReactionSet()
    
    r1 = lab.new_reaction('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=1.0, bounds=(0.0, 10.0))
    k2 = r1.parameter('k2', value=0.224, bounds=(0.0, 10.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1e-3)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    # Use this function to replace the old filename set-up
    r1.add_data(category='spectral', file='data/Dij_exp1.txt')
    
    # Preprocessing!
    #r1.spectra.msc()
    #r1.spectra.decrease_wavelengths(2)

    # define explicit system of ODEs
    rA = k1*A
    rB = k2*B
    
    # Define the reaction model
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    
    # Settings
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 100
    r1.settings.parameter_estimator.scaled_variance = False
    r1.spectra.decrease_wavelengths(4)

   
    # Repeat for the second model - the only difference is the dataset    
    r2 = lab.new_reaction(name='reaction-2', model=r1)

    # Add the dataset for the second model
    r2.add_data(file='data/Dij_exp3_reduced.txt', category='spectral')
    r2.spectra.decrease_wavelengths(4)

    """Using confidence intervals - uncomment the following three lines"""
    lab.settings.parameter_estimator.covariance = 'ipopt_sens'
    lab.settings.general.shared_spectra = True
    
    # Create the MultipleExperimentsEstimator and perform the parameter fitting
    lab.run_opt()

    # Plot the results
    if with_plots:    
        lab.report()