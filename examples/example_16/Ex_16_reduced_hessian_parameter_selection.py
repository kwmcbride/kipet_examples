"""
Example 16: Parameter Selection Using the Reduced Hessian

Kipet: Kinetic parameter estimation toolkit
Copyright (c) 2016 Eli Lilly.
 
Example from Chen and Biegler, Reduced Hessian Based Parameter Selection and
    Estimation with Simultaneous Collocation Approach (AIChE 2020) paper with
    a CSTR for a simple reaction.
    
This example uses reactor temperature as the known output data as well as some
concentration data.
"""
# Standard library imports
import sys

# Third party imports
from pyomo.environ import exp

# Kipet library imports
import kipet
                                                                                                    
if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2 and int(sys.argv[1]):
        with_plots = False
    
    r1 = kipet.ReactionModel('cstr')
    
    r1.unit_base.time = 'hr'
    r1.unit_base.volume = 'm**3'
    
    # Perturb the initial parameter values by some factor
    factor = 1.2
    
    # Add the model parameters
    Tf = r1.parameter('Tf', value=293.15*factor, bounds=(250, 350), units='K')
    Cfa = r1.parameter('Cfa', value=2500*factor, bounds=(100, 5000), units='mol/m**3')
    rho = r1.parameter('rho', value=1025*factor, bounds=(800, 1100), units='kg/m**3')
    delH = r1.parameter('delH', value=160*factor, bounds=(10, 400), units='kJ/mol')
    ER = r1.parameter('ER', value=255*factor, bounds=(10, 500), units='K')
    k = r1.parameter('k', value=2.5*factor, bounds=(0.1, 10), units='1/hour')
    Tfc = r1.parameter('Tfc', value=283.15*factor, bounds=(250, 350), units='K')#, fixed=True)
    rhoc = r1.parameter('rhoc', value=1000*factor, bounds=(800, 2000), units='kg/m**3')#, fixed=True)
    h = r1.parameter('h', value=1000*factor, bounds=(10, 5000), units='W/m**2/K')#, fixed=True)
    
    # Declare the components and give the valueial values
    A = r1.component('A', value=1000, variance=0.001, units='mol/m**3')
    T = r1.state('T', value=293.15, variance=0.0625,  units='K')
    Tc = r1.state('Tc', value=293.15, variance=0.001, units='K')
   
    # Change this to a clearner method
    full_data = kipet.read_data('data/all_data.csv')
    
    F = r1.constant('F', value=0.1, units='m**3/hour')
    Fc = r1.constant('Fc', value=0.15, units='m**3/hour')
    Ca0 = r1.constant('Ca0', value=1000, units='mol/m**3')
    V = r1.constant('V1', value=0.2, units='m**3')
    Vc = r1.constant('Vc', value=0.055, units='m**3')
    Ar = r1.constant('Area', value=4.5, units='m**2')
    Cpc = r1.constant('Cpc', value=1.2, units='kJ/kg/K')
    Cp = r1.constant('Cp', value=1.55, units='kJ/kg/K')
    
    r1.add_data('T_data', data=full_data[['T']], time_scale='hour')
    #r1.add_data('A_data', data=full_data[['A']].loc[[3.9, 2.6, 1.115505]], time_scale='hour')
    
    # Not really necessary, but useful for tracking
    rA = r1.add_reaction('rA', k*exp(-ER/T)*A, description='Reaction A' )
    
    r1.add_ode('A', F/V*(Cfa - A) - rA )
    r1.add_ode('T', F/V *(Tf - T) + delH/rho/Cp*rA - h*Ar/rho/Cp/V*(T -Tc) )
    r1.add_ode('Tc', Fc/Vc *(Tfc - Tc) + h*Ar/rhoc/Cpc/Vc*(T -Tc) )
    
    # Convert the units
    r1.check_model_units(display=True)
    
    r1.settings.solver.print_level = 5
    r1.settings.collocation.ncp = 1
    r1.settings.collocation.nfe = 150
    
    rh_method = 'fixed'
    results = r1.rhps_method(method='k_aug',
                             calc_method=rh_method,
                             scaled=True)
