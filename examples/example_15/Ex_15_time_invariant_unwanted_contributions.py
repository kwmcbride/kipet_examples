"""Example 15: Time invariant unwanted contributions with the new KipetModel
 
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports
import pandas as pd

# Kipet library imports
import kipet
                                                                                                    
if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('reaction-1')
    
    # Add the model parameters
    k1 = r1.parameter('k1', value=1.4, bounds=(0.0, 2.0))
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
    
     # Add the data
    r1.add_data(category='spectral', file='data/Dij_tiv_G.txt')
    
    # Settings
    r1.settings.collocation.nfe = 100
  
    # In this case, there is no dosing time. 
    # Therefore, the following expression just an input example 
    # if the user has dosing concentraion in the model.
    # Z_in = dict()
    # Z_in["t=5"] = [0,0,5]

    r1.unwanted_contribution('time_invariant_G')

    # Run KIPET
    r1.run_opt()
    r1.results.show_parameters

    if with_plots:
        r1.report()
        
    """We can now compare the results with the known profiles"""
    
    # Read the true S to compare with results
    S_true_filename = 'data/S_True_for_unwanted_G.csv'
    S_True = kipet.read_data(S_true_filename)

    # In this example, we know the magnitude of unwanted contribution.
    # Therefore, we can calculate the matched S according to "" to compare the results.
    index = list(S_True.index)
    column = list(S_True.columns)
    data = []
    for i in index:
        sgi = 2.5E-6*i/0.01
        row = [sgi,sgi,sgi]
        data.append(row)
        
    Sg = pd.DataFrame(data, columns = column, index = index)
    S_matched = S_True + Sg
    # Make sure the columns have the same names as in the original
    S_matched.columns = ['A', 'B', 'C']
        
    """
    This is currently unavailable
    
    # # Use the "label" kwarg to add some info to the legend in the plot
    #if with_plots:
    #    r1.results.plot('S', show_plot=with_plots, extra_data={'data': S_matched, 'label': 'matched'})  
    """