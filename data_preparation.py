import numpy as np
import pandas as pd

def load_and_prepare_data(capacities_path, efficiencies_path, mc_path, co2_path, ger_pp_path, nuts1_path, wind_path, pv_path, load_path, charge_path, discharge_path, hydro_charge_path, hydro_discharge_path):
    # Load data from CSV files
    capacities_federal_states = pd.read_csv(capacities_path)
    efficiencies_federal_states = pd.read_csv(efficiencies_path)
    mc_federal_states = pd.read_csv(mc_path)
    co2_federal_states = pd.read_csv(co2_path)
    ger_pp = pd.read_csv(ger_pp_path)
    nuts1 = pd.read_csv(nuts1_path)
    wind = pd.read_csv(wind_path)
    pv = pd.read_csv(pv_path)
    load = pd.read_csv(load_path)
    charge = pd.read_csv(charge_path)
    discharge = pd.read_csv(discharge_path)
    hydro_charge = pd.read_csv(hydro_charge_path)
    hydro_discharge = pd.read_csv(hydro_discharge_path)

    # Data preparation steps
    efficiency = capacities_federal_states.groupby(by='Fueltype')['Efficiency'].mean()
    efficiencies_federal_states.fillna(efficiency, inplace=True)

    marginal_costs = ger_pp.groupby(by='Fueltype')['MarginalCosts'].mean()
    mc_federal_states.fillna(marginal_costs, inplace=True)

    marginal_co2 = ger_pp.groupby(by='Fueltype')['MarginalCO2'].mean()
    co2_federal_states.fillna(marginal_co2, inplace=True)

    capacities_federal_states = ger_pp.groupby(by=['NUTS_NAME', 'Fueltype'])['Capacity'].sum()
    efficiencies_federal_states = ger_pp.groupby(by=['NUTS_NAME', 'Fueltype'])['Efficiency'].mean()
    mc_federal_states = ger_pp.groupby(by=['NUTS_NAME', 'Fueltype'])['MarginalCosts'].mean()
    co2_federal_states = ger_pp.groupby(by=['NUTS_NAME', 'Fueltype'])['MarginalCO2'].mean()

    capacities_federal_states = capacities_federal_states.unstack().fillna(0)
    efficiencies_federal_states = efficiencies_federal_states.unstack().fillna(0)
    mc_federal_states = mc_federal_states.unstack().fillna(0)
    co2_federal_states = co2_federal_states.unstack().fillna(0)

    return capacities_federal_states, efficiencies_federal_states, mc_federal_states, co2_federal_states, ger_pp, nuts1, wind, pv, load, charge, discharge, hydro_charge, hydro_discharge

def save_prepared_data(capacities, efficiencies, mc, co2):
    capacities.to_csv('capacities_federal_states_prepared.csv')
    efficiencies.to_csv('efficiencies_federal_states_prepared.csv')
    mc.to_csv('mc_federal_states_prepared.csv')
    co2.to_csv('co2_federal_states_prepared.csv')
