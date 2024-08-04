import pyomo.environ as pyo
import numpy as np
import pandas as pd

def create_optimization_model(capacities_federal_states, mc_federal_states, co2_federal_states, load):
    Z = 2
    Time = 8760
    G = len(capacities_federal_states)

    Z = np.array([n for n in range(0, Z)])
    T = np.array([n for n in range(0, Time)])
    G = np.array([n for n in range(0, G)])
    T1 = np.array([n for n in range(1, Time)])

    m1 = pyo.ConcreteModel()
    m1.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

    # Define sets
    m1.G = pyo.Set(initialize=G)
    m1.T = pyo.Set(initialize=T)
    m1.T1 = pyo.Set(initialize=T1)

    # Define parameters
    cap_fed = np.array(capacities_federal_states)
    mc_fed = np.array(mc_federal_states)
    co2_fed = np.array(co2_federal_states)
    m1.Load = pyo.Param(m1.T, initialize=load.to_dict())

    # Define variables
    m1.Gen = pyo.Var(m1.G, m1.T, domain=pyo.NonNegativeReals)
    m1.Soc = pyo.Var(m1.T, domain=pyo.NonNegativeReals)
    m1.charge = pyo.Var(m1.T, domain=pyo.NonNegativeReals)
    m1.discharge = pyo.Var(m1.T, domain=pyo.NonNegativeReals)
    m1.Hydro_Soc = pyo.Var(m1.T, domain=pyo.NonNegativeReals)
    m1.Hydro_charge = pyo.Var(m1.T, domain=pyo.NonNegativeReals)
    m1.Hydro_discharge = pyo.Var(m1.T, domain=pyo.NonNegativeReals)

    # Define objective function
    m1.costs = pyo.Objective(expr=sum(m1.Gen[g, t] * mc_fed[g] for g in m1.G for t in m1.T), sense=pyo.minimize)

    # Define constraints
    m1.Cap_ub = pyo.Constraint(m1.G, m1.T, rule=lambda m, g, t: m1.Gen[g, t] <= cap_fed[g])
    m1.Cap_lb = pyo.Constraint(m1.G, m1.T, rule=lambda m, g, t: m1.Gen[g, t] >= 0)

    # BESS constraints
    SOC_max = 100000
    n = 0.8
    m1.BESS = pyo.Constraint(m1.T1, rule=lambda m1, t: m1.Soc[t] == m1.Soc[t-1] + m1.charge[t] * n - m1.discharge[t])
    m1.BESS_lb = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Soc[t] >= 0)
    m1.BESS_ub = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Soc[t] <= SOC_max)
    m1.BESS_charge_up = pyo.Constraint(m1.T, rule=lambda m1, t: m1.charge[t] <= SOC_max / 10)
    m1.BESS_discharge_up = pyo.Constraint(m1.T, rule=lambda m1, t: m1.discharge[t] <= SOC_max / 10)
    m1.Soc[0] = SOC_max / 2
    m1.Soc[Time - 1] = SOC_max / 2

    # Pumped hydro constraints
    n = 0.9
    Hydro_max = 10000
    m1.Hydro = pyo.Constraint(m1.T1, rule=lambda m1, t: m1.Hydro_Soc[t] == m1.Hydro_Soc[t-1] + m1.Hydro_charge[t] * n - m1.Hydro_discharge[t])
    m1.Hydro_lb = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Hydro_Soc[t] >= 0)
    m1.Hydro_ub = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Hydro_Soc[t] <= Hydro_max)
    m1.Hydro_charge_up = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Hydro_charge[t] <= Hydro_max / 10)
    m1.Hydro_discharge_up = pyo.Constraint(m1.T, rule=lambda m1, t: m1.Hydro_discharge[t] <= Hydro_max / 10)
    m1.Hydro_Soc[0] = Hydro_max / 2
    m1.Hydro_Soc[Time - 1] = Hydro_max / 2

    return m1

def solve_model(m1):
    solver = pyo.SolverFactory('glpk')
    solver.solve(m1)
    return m1
