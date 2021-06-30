"""Example 9: Data generation and estimability analysis

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
   
    """Simulation Model for generating data""" 
   
    sim_model = kipet.ReactionModel('simulation')
    
    A = sim_model.component('A', value=0.5)
    B = sim_model.component('B', value=0.0)
    C = sim_model.component('C', value=0.0)
    D = sim_model.component('D', value=0.01)
    E = sim_model.component('E', value=0.0)
    F = sim_model.component('F', value=0.3)
    G = sim_model.component('G', value=0.5)
    H = sim_model.component('H', value=0.0)
    
    #Following this we add the kinetic parameters
    k1 = sim_model.parameter('k1', value=0.3)
    k2 = sim_model.parameter('k2', value=0.1)
    k3 = sim_model.parameter('k3', value=0.1)
    k4 = sim_model.parameter('k4', value=0.4)
    k5 = sim_model.parameter('k5', value=0.02)
    k6 = sim_model.parameter('k6', value=0.5)
    
    
    sim_model.add_ode('A', -k1*A - k4*A - k5*E*A )
    sim_model.add_ode('B',  k1*A - k2*B - k3*B )
    sim_model.add_ode('C',  k2*B - k4*C )
    sim_model.add_ode('D',  k4*A - k3*D )
    sim_model.add_ode('E',  k3*B - k5*E*A )
    sim_model.add_ode('F',  k5*E*A - k6*G**2*F )
    sim_model.add_ode('G', -k6*G**2*F )
    sim_model.add_ode('H',  k6*G**2*F )
    
    # sim_model.add_equations(rule_odes)
    sim_model.set_time(20)
    sim_model.simulate()
    
    #if with_plots:
        #sim_model.report()

    # Add some noise and save the data
    data = kipet.add_noise_to_data(sim_model.results.Z, 0.02)
    filename = 'data/sim_data.csv'
    kipet.write_data(filename, data)
    
    """Make the model for estimability analysis"""
    
    # Clone the simulation model for the estimability analysis
    r1 = kipet.ReactionModel('reaction-1', model=sim_model)
    
    # Add the generated data
    r1.add_data('C_data', category='concentration', file=filename)

    # Change the parameter initial values and add bounds
    new_inits = {
        'k1': 0.2,
        'k2': 0.2,
        'k3': 0.05,
        'k4': 0.5,
        'k5': 0.032,
        'k6': 0.45,
    }
    
    new_bounds = {k: (0, 1) for k in r1.parameters.names}
    
    r1.parameters.update('value', new_inits)
    r1.parameters.update('bounds', new_bounds)

    # This is used for scaling the variables (i.e. 0.01 means that we are sure that the initial 
    # value ofthat parameter is within 1 % of the real value)
    param_uncertainties = {'k1':0.8,'k2':1.2,'k3':0.8,'k4':0.4, 'k5':1,'k6':0.3}
    # sigmas, as before, represent the variances in regard to component
    sigmas = {'A':1e-10,'B':1e-10,'C':1e-11, 'D':1e-11,'E':1e-11,'F':1e-11,'G':1e-11,'H':1e-11,'device':0.02}
    # measurement scaling
    meas_uncertainty = 0.02
    
    params_fit, params_fix = r1.analyze_parameters(
        method='yao',
        parameter_uncertainties=param_uncertainties,
        meas_uncertainty=meas_uncertainty,
        sigmas=sigmas
    )
 
    """Run the PE again - this could just be run using the r1 model"""
    
    # Clone the simulation model without the model
    final_model = kipet.ReactionModel('final', model=sim_model)

    # Add bounds to the parameter variables and change k5 to 0.032
    final_model.parameters.update('bounds', new_bounds)
    final_model.parameters.update('value', {'k5' : 0.032})
    
    # Update the component variances provided above
    final_model.components.update('variance', sigmas)
    
    # Add the experimental data
    final_model.add_data('C_data', category='concentration', file=filename)
    
    # Settings
    final_model.settings.parameter_estimator.solver = 'ipopt'
    
    # Fix the parameter that cannot be estimated here:
    final_model.fix_parameter(params_fix)
    
    # Run the parameter estimation
    final_model.run_opt()
    
    # Results and plot
    final_model.results.show_parameters
    if with_plots:
        final_model.plot()
