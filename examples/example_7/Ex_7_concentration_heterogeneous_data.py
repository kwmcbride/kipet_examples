"""
Example 7: Estimation using measured concentration data with different
measurement points
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
    k1 = r1.parameter('k1', value=2.0, bounds=(0.0, 5.0))
    k2 = r1.parameter('k2', value=0.2, bounds=(0.0, 2.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=0.001, known=False, bounds=(0, 3))
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
   
    # Use this function to replace the old filename set-up
    filename = 'data/missing_data_no_start.txt'
    r1.add_data(file=filename)
    
    rA = k1*A
    rB = k2*B
    
    # Define the reaction model
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    
    # Settings
    r1.settings.collocation.nfe = 60
    
    # Run KIPET
    r1.run_opt()  
    
    # Display the results
    r1.results.show_parameters

    if with_plots:
        r1.plot()
