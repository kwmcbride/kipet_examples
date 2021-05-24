"""
Example 7: Estimation using measured concentration data and unknown reaction
start
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
    A = r1.component('A', value=0.001, variance=1e-10)
    B = r1.component('B', value=0.0, variance=1e-11)
    C = r1.component('C', value=0.0, variance=1e-8)
    
    #V = r1.volume(value=1)
   
    # Load data and reduce the number of data points used
    filename = 'data/delayed_data.csv'
    full_data = kipet.read_data(filename)
    
    data_set = full_data.iloc[::3]
    r1.add_data('C_data', data=data_set)
    
    # Use step functions to turn on the reactions
    b1 = r1.step('b1', time=2, fixed=False, switch='on')
    # Alternatively you can use a second binary switch
    # b2 = r1.step('b2', time=2.1, fixed=True, switch='on')
    
    rA = b1*(k1*A)
    rB = b1*(k2*B)
    
    # Define the reaction model
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )
    
    # Settings
    r1.settings.collocation.nfe = 60
    r1.settings.collocation.ncp = 3
    
    # Run KIPET
    r1.run_opt()  
    
    # Display the results
    r1.results.show_parameters

    if with_plots:
        r1.plot()
