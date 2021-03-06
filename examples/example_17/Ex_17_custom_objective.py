"""
Example 17: Using custom data in the objective

This example uses data representing the ratio of component B to the total of
B and C (B/(B+C)). This data is entered into the model with the category
custom. The ratio between B and C is then entered as an algebraic rule and the
variable describing this ratio, y, is given as a custom objective. The least
squares difference between y and the provided data is added to the objective
function.

"""
import sys

import kipet

if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('reaction-1')
    r1.unit_base.time = 's'
    
    full_data = kipet.read_data('data/ratios.csv')

    # Add the model parameters
    k1 = r1.parameter('k1', value=2, bounds=(0.0, 10.0), units='1/s')
    k2 = r1.parameter('k2', value=0.2, bounds=(0.0, 10.0), units='1/s')
    
    # Declare the components and give the valueial values
    A = r1.component('A', value=1.0, units='mol/l')
    B = r1.component('B', value=0.0, units='mol/l')
    C = r1.component('C', value=0.0, units='mol/l')
    
    # The following has been automated throught the add_expression method
    #y = r1.algebraic('y', description='Ratio of B to B + C')
    
    r1.add_data('C_data', data=full_data[['A']], remove_negatives=True)
    r1.add_data('y_data', data=full_data[['y']])
    
    r1.add_ode('A', -k1 * A )
    r1.add_ode('B', k1 * A - k2 * B )
    r1.add_ode('C', k2 * B )
    
    r1.add_expression('y', B/(B + C), description='Ratio of B to (B + C)' )
    
    r1.check_model_units()
    
    # Add the custom objective varibale to the model using the following method:
    r1.add_objective_from_algebraic('y')
     
    # Run optimization
    r1.run_opt()
    
    r1.results.show_parameters
    
    if with_plots:
        r1.plot()
