"""
Advanced Demonstration 13: How to solve problems with unknown initial conditions
"""
# Standard library imports
import sys

# Third party imports

# KIPET library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    lab = kipet.ReactionLab()
 
    r1 = lab.new_reaction('reaction-1')   
 
    # Add the model parameters
    k1 = r1.parameter('k1', value=1.0, bounds=(0.0, 10.0), fixed=False)
    k2 = r1.parameter('k2', value=0.224, bounds=(0.0, 10.0), fixed=False)
    
    # Declare the components and give the initial values
    A = r1.component('A', value=0.001, known=False, bounds=(0.0, 0.1))
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
   
    # Use this function to replace the old filename set-up
    filename = 'data/Ex_1_C_data_withoutA.csv'
    
    r1.add_data(file=filename)
    
    # Define the reaction model
    r1.add_ode('A', -k1 * A )
    r1.add_ode('B', k1 * A - k2 * B )
    r1.add_ode('C', k2 * B )
    
    # Repeat for the second model - the only difference is the dataset    
    r2 = lab.new_reaction(name='reaction-2', model=r1)
    # Simulated second dataset with noise
    noised_data = kipet.add_noise_to_data(r1.datasets['ds-1'].data, 0.0001) 
    
    # Add the dataset for the second model
    r2.add_data(data=noised_data)

    lab.settings.solver.solver = 'ipopt_sens'

    r1.variances = {'device':1e-10,'A':1e-10,'B':1e-10,'C':1e-10}
    r2.variances = {'device':1e-4,'A':1e-4,'B':1e-4,'C':1e-4}
    
    lab.run_opt()
    
    # Plot the results
    if with_plots:
        lab.show_parameters
        lab.plot()
