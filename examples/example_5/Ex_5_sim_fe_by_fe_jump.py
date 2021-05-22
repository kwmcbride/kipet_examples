"""
Example 5: Simulation with extra states and dosing

"""
# Standard library imports
import sys # Only needed for running the example from the command line

# Kipet library imports
import kipet


if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('simulation')
    r1.unit_base.time = 'min'
    
    # Components
    AH = r1.component('AH', value= 0.395555)
    B = r1.component('B', value= 0.0351202)
    C = r1.component('C', value= 0.0)
    BHp = r1.component('BHp', value= 0.0)
    Am = r1.component('Am', value= 0.0)
    ACm = r1.component('ACm', value= 0.0)
    P = r1.component('P', value= 0.0)
    
    # Parameters
    k0 = r1.parameter('k0', value=49.7796)
    k1 = r1.parameter('k1', value=8.93156)
    k2 = r1.parameter('k2', value=1.31765)
    k3 = r1.parameter('k3', value=0.31087)
    k4 = r1.parameter('k4', value=3.87809)
    
    # States
    V = r1.state('V', state='state', value=0.0629418)
    
    # Stoichiometric coefficients
    stoich_coeff = dict()
    stoich_coeff['AH'] = [-1, 0, 0, -1, 0]
    stoich_coeff['B'] = [-1, 0, 0, 0, 1]
    stoich_coeff['C'] = [0, -1, 1, 0, 0]
    stoich_coeff['BHp'] = [1, 0, 0, 0, -1]
    stoich_coeff['Am'] = [1, -1, 1, 1, 0]
    stoich_coeff['ACm'] = [0, 1, -1, -1, -1]
    stoich_coeff['P'] = [0, 0, 0, 1, 1]
    
    V_step = r1.step('V_step', time=210, fixed=True, switch='off')
    V_flow = r1.constant('V_flow', value=7.27609e-5)
    
    y0 = r1.add_reaction('y0', k0*AH*B, description='Reaction 0')
    y1 = r1.add_reaction('y1', k1*Am*C, description='Reaction 1')
    y2 = r1.add_reaction('y2', k2*ACm, description='Reaction 2')
    y3 = r1.add_reaction('y3', k3*ACm*AH, description='Reaction 3')
    y4 = r1.add_reaction('y4', k4*ACm*BHp, description='Reaction 4')
    
    RE = r1.reactions_from_stoich(stoich_coeff, add_odes=False)
    # Modify component C
    RE['C'] += 0.02247311828 / (V * 210) * V_step
    
    # Add the volume change to each component ODE
    for com in r1.components.names:
        RE[com] -= V_flow*V_step/V*r1.components[com].pyomo_var
    
    # ODEs
    r1.add_odes(RE)
    r1.add_ode('V', V_flow*V_step)
    
    # Add dosing points (as many as you want in this format)
    # ('component_name', time, amount)
    r1.add_dosing_point('AH', 100, 0.3)
    
    # Simulations require a time span
    r1.set_time(600)
    
    # Settings
    r1.settings.collocation.nfe = 40
    r1.settings.simulator.method = 'fe'
    
    # Perform simulation
    r1.simulate()
    
    # Create plots
    if with_plots:
        r1.plot()
