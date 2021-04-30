"""Example 2: Estimation with new KipetModel"""

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
 
    
    # You need to solve a smaller model
    # Pass the parameters to the new model
    # Re-optimize the second model
    
    kipet_model = KipetModel()
    
    r1 = kipet_model.new_reaction('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=0.3, bounds=(0.0, 5.0))
    k2 = r1.parameter('k2', value=1.4, bounds=(0.0, 3.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    
    file_name = '/home/kevin/Dev/kipet_examples/examples/example_2/data/Dij.txt'
    full_data = kipet_model.read_data_file(file_name)

    wl_reduction = 1
    ts_reduction = 1

    small_data = full_data.loc[::ts_reduction, ::wl_reduction]
    
    # Use this function to replace the old filename set-up
    r1.add_data(category='spectral', data=small_data)
    
    # Preprocessing!
    #r1.spectra.msc()
    r1.spectra.decrease_wavelengths(1)

    # define explicit system of ODEs
    rates = {}
    rates['A'] = -k1 * A
    rates['B'] = k1 * A - k2 * B
    rates['C'] = k2 * B
    
    r1.add_odes(rates)
    
    r1.bound_profile(var='S', bounds=(0, 10))

    # Settings
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 60
    r1.settings.parameter_estimator.tee = True
    r1.settings.parameter_estimator.solver = 'ipopt'
    #r1.settings.general.initialize_pe = True
    #r1.settings.general.scale_pe = True
    r1.settings.parameter_estimator.sim_init = False
        
    
    r1.run_opt()
    r1.plot('Z')
    
    
 