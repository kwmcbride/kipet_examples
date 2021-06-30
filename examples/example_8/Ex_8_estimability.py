"""
Example 8: Using the estimability analysis tools
""" 
# Standard libary imports
import sys

# Kipet library imports
import kipet


if __name__ == "__main__":
 
    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False   

    r1 = kipet.ReactionModel('reaction-1')   
     
    # Add the model parameters
    k1 = r1.parameter('k1', value=1.2, bounds=(0.1,2))
    k2 = r1.parameter('k2', bounds=(0.0,2))
    k3 = r1.parameter('k3', bounds=(0.0,2))
    k4 = r1.parameter('k4', bounds=(0.0,2))
    
    # Declare the components and give the initial values
    A = r1.component('A', value=0.3)
    B = r1.component('B', value=0.0)
    C = r1.component('C', value=0.0)
    D = r1.component('D', value=0.01)
    E = r1.component('E', value=0.0)
    
    filename = 'data/new_estim_problem_conc.csv'
    r1.add_data('C_frame', file=filename) 
    
    r1.add_ode('A', -k1*A - k4*A )
    r1.add_ode('B',  k1*A - k2*B - k3*B )
    r1.add_ode('C',  k2*B - k4*C )
    r1.add_ode('D',  k4*A - k3*D )
    r1.add_ode('E',  k3*B )
    
    r1.set_time(20)
    
    r1.make_model()
    
    # r1.report()
    # r1.plot('Z', show=True)
    
    # r1.settings.simulator.simulator = 'dae.collocation'
    
    #%%
    param_uncertainties = {'k1':0.09,'k2':0.01,'k3':0.02,'k4':0.5}
    sigmas = {'A':1e-10,'B':1e-10,'C':1e-11, 'D':1e-11,'E':1e-11,'device':3e-9}
    meas_uncertainty = 0.05
    
    from kipet.estimability_tools.estimability_analysis import EstimabilityAnalyzer
    
    model = r1._model
    
    
    r1.e_analyzer = EstimabilityAnalyzer(model)
    
    
    #%%
    # e = r1.e_analyzer
    
    r1.e_analyzer.apply_discretization('dae.collocation',
                                                  nfe=60,
                                                  ncp=3,
                                                  scheme='LAGRANGE-RADAU')
         
    #%%
       
    # #%%
    listparams = r1.e_analyzer.rank_params_yao(meas_scaling=meas_uncertainty,
                                                              param_scaling=param_uncertainties,
                                                              sigmas=sigmas)

#%%

    
    #%%
    # #print(listparams)
    # listparams = [p for p in r1._model.P] 
    # # Now we can run the analyzer using the list of ranked parameters
    # params_to_select = r1.e_analyzer.run_analyzer(method='Wu', 
    #                                                 parameter_rankings=listparams,
    #                                                 meas_scaling=meas_uncertainty, 
    #                                                 variances=sigmas
    #                                                 )
    
    #%%
    
    # params_fit, params_fix = r1.analyze_parameters(
    #     method='yao',
    #     parameter_uncertainties=param_uncertainties,
    #     meas_uncertainty=meas_uncertainty,
    #     sigmas=sigmas
    # )
