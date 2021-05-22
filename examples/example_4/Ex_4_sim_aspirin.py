"""
Example 4: Simulated Asprin with fixed states and stoichiometric matrix
"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports
from pyomo.core import exp

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    rm = kipet.ReactionModel('reaction-1')

    # Components
    SA = rm.component('SA', value=1.0714, description='Salicitilc acid')
    AA = rm.component('AA', value=9.3828, description='Acetic anhydride')
    ASA = rm.component('ASA', value=0.0177, description='Acetylsalicylic acid')
    HA = rm.component('HA', value=0.0177, description='Acetic acid')
    ASAA = rm.component('ASAA', value=0.000015, description='Acetylsalicylic anhydride')
    H2O = rm.component('H2O', value=0.0, description='Water')
    
    # Parameters
    k0 = rm.parameter('k0', value=0.0360309)
    k1 = rm.parameter('k1', value=0.1596062)
    k2 = rm.parameter('k2', value=6.8032345)
    k3 = rm.parameter('k3', value=1.8028763)
    kd = rm.parameter('ks', value=7.1108682)
    kc = rm.parameter('kc', value=0.7566864)
    Csa = rm.parameter('Csa',value=2.06269996)
    
    # Additional state variables
    V = rm.state('V', value=0.0202)
    Masa = rm.state('Masa', value=0.0)
    Msa = rm.state('Msa', value=9.537)
    
    # Fixed states (data is provided using the data keyword argument)
    f = rm.fixed_state('f', description='flow f', data='traj')
    Csat = rm.fixed_state('Csat', description='C saturation', data='traj')
    
    # Stoichiometric matrix (component based)
    gammas = dict()
    gammas['SA']=    [-1, 0, 0, 0, 1, 0]
    gammas['AA']=    [-1,-1, 0,-1, 0, 0]
    gammas['ASA']=   [ 1,-1, 1, 0, 0,-1]
    gammas['HA']=    [ 1, 1, 1, 2, 0, 0]
    gammas['ASAA']=  [ 0, 1,-1, 0, 0, 0]
    gammas['H2O']=   [ 0, 0,-1,-1, 0, 0]

    epsilon = dict()
    epsilon['SA']= 0.0
    epsilon['AA']= 0.0
    epsilon['ASA']= 0.0
    epsilon['HA']= 0.0
    epsilon['ASAA']= 0.0
    epsilon['H2O']= 1.0
    
    partial_vol = dict()
    partial_vol['SA']=0.0952552311614
    partial_vol['AA']=0.101672206869
    partial_vol['ASA']=0.132335206093
    partial_vol['HA']=0.060320218688
    partial_vol['ASAA']=0.186550717015
    partial_vol['H2O']=0.0883603912169

    # Adding data
    filename = 'data/extra_states.txt'
    rm.add_data('traj', category='trajectory', file=filename)
    
    filename = 'data/concentrations.txt'
    rm.add_data('conc', category='trajectory', file=filename)
    
    filename = 'data/init_Z.csv'
    rm.add_data('init_Z', category='trajectory', file=filename)
    
    filename = 'data/init_X.csv'
    rm.add_data('init_X', category='trajectory', file=filename)
    
    filename = 'data/init_Y.csv'
    rm.add_data('init_Y', category='trajectory', file=filename)

    # Reactions
    r0 = rm.add_reaction('r0', k0*SA*AA, description='Reaction 0')
    r1 = rm.add_reaction('r1', k1*ASA*AA, description='Reaction 1' )
    r2 = rm.add_reaction('r2', k2*ASAA*H2O, description='Reaction 2' )
    r3 = rm.add_reaction('r3', k3*AA*H2O, description='Reaction 3')
    
    step = 1/(1 + exp(-Msa/1e-4))
    r4 = rm.add_reaction('r4', kd*(Csa - SA + 1e-6)**1.90*step, description='Reaction 4' )
    
    diff = ASA - Csat
    r5 = rm.add_reaction('r5', 0.3950206559*kc*(diff+((diff)**2+1e-6)**0.5)**1.34, description='Reaction 5' )
    
    # Generate the ODEs for the reactions based on the stoichiometric matrix
    # Since we need to modfiy the ODEs, add_odes should be False
    odes = rm.reactions_from_stoich(gammas, add_odes=False)
    
    v_sum_float = 0
    Cin = 39.1
    
    # Build expression for the volume
    for com in rm.components.names:
        v_sum_float += partial_vol[com] * (odes[com] + epsilon[com]*f/V*Cin)
    
    v_sum = rm.add_expression('v_sum', v_sum_float, description='Volume Sum')
    
    # If calling a component (such as A or B) in a loop, use the pyomo_var attribute
    # Add ODEs for the components
    for com in rm.components.names:
        rm.add_ode(com, odes[com] + epsilon[com]*f/V*Cin - v_sum*rm.components[com].pyomo_var)
    
    # Add ODEs for complementary states
    rm.add_ode('V', V*v_sum )
    rm.add_ode('Masa', 180.157*V*r5 )
    rm.add_ode('Msa', -138.121*V*r4 )

    # Simulations require a time span
    rm.set_time(210.5257)

    # Settings
    rm.settings.collocation.nfe = 100
    rm.settings.simulator.solver_opts.update({'halt_on_ampl_error' :'yes'})
    
    # Initialize the model variables with the provided data
    rm.initialize_from_trajectory('Z', 'init_Z')
    rm.initialize_from_trajectory('X', 'init_X')
    rm.initialize_from_trajectory('Y', 'init_Y')

    # Run the simulation
    rm.simulate()

    # # Plot the results
    if with_plots:
        rm.plot('Z')