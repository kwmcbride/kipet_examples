"""
Example 2: Simple example showing parameter fitting using spectral data
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    rs = kipet.ReactionSet()
    
    r1 = kipet.ReactionModel('reaction-1')

    # Add the model parameters
    k1 = r1.parameter('k1', value=4.0, bounds=(0.0, 5.0))
    k2 = r1.parameter('k2', value=0.5, bounds=(0.0, 2.0))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=1e-3)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    
    # Input data
    file_name = 'data/Dij.txt'
    r1.add_data(category='spectral', file=file_name)
    
    a_data = kipet.read_data('data/uplc.csv')
    a_data = a_data[['A']]
    a_data.columns = ['y']
    #r1.add_data('y_data', data=a_data)
    
    #r1.add_data(category='uplc', file='data/uplc.csv')

    # Input the reactions as expressions
    rA = r1.add_reaction('rA', k1*A)
    rB = r1.add_reaction('rB', k2*B)
    
    # Input the ODEs
    r1.add_ode('A', -rA )
    r1.add_ode('B', rA - rB )
    r1.add_ode('C', rB )

    # Change some of the default settings
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 60
    r1.settings.parameter_estimator.tee = True
    r1.settings.parameter_estimator.solver = 'ipopt'
    
    # r1.settings.parameter_estimator.with_d_vars = True
    
    # Parameter fitting
    r1.run_opt()
    
    r1.results.show_parameters
    # Create plots
    if with_plots:
        r1.plot('Z')
        
    lof = r1.p_estimator.lack_of_fit()
        
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
    