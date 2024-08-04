
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import model
import data_preparation

# Define file paths
capacities_path = 'path/to/capacities_federal_states.csv'
efficiencies_path = 'path/to/efficiencies_federal_states.csv'
mc_path = 'path/to/mc_federal_states.csv'
co2_path = 'path/to/co2_federal_states.csv'
ger_pp_path = 'path/to/ger_pp.csv'
nuts1_path = 'path/to/nuts1.csv'
wind_path = 'path/to/wind.csv'
pv_path = 'path/to/pv.csv'
load_path = 'path/to/load.csv'
charge_path = 'path/to/charge.csv'
discharge_path = 'path/to/discharge.csv'
hydro_charge_path = 'path/to/hydro_charge.csv'
hydro_discharge_path = 'path/to/hydro_discharge.csv'

# Load and prepare data
capacities_federal_states, efficiencies_federal_states, mc_federal_states, co2_federal_states, ger_pp, nuts1, wind, pv, load, charge, discharge, hydro_charge, hydro_discharge = data_preparation.load_and_prepare_data(
    capacities_path, efficiencies_path, mc_path, co2_path, ger_pp_path, nuts1_path, wind_path, pv_path, load_path, charge_path, discharge_path, hydro_charge_path, hydro_discharge_path)

data_preparation.save_prepared_data(capacities_federal_states, efficiencies_federal_states, mc_federal_states, co2_federal_states)

# Create and solve the optimization model
m1 = model.create_optimization_model(capacities_federal_states, mc_federal_states, co2_federal_states, load)
solved_model = model.solve_model(m1)

# Results extraction and visualization
gen_winter_day = pd.DataFrame()
for t in np.arange(120, 144):
    gen_winter_day[t] = [pyo.value(solved_model.Gen[g, t]) for g in solved_model.G]

gen_winter_day.index = capacities_federal_states.index
dispatch_day_winter = gen_winter_day.groupby(by='Fueltype').sum().T
dispatch_day_winter.columns = gen_winter_day.groupby(by='Fueltype').sum().T.columns[:]
dispatch_day_winter.reset_index(inplace=True)
dispatch_day_winter.to_csv('dispatch_day_winter.csv')

# Plotting results for winter day
hours = np.arange(0, 24)
plt.figure(figsize=(10, 6))
plt.stackplot(hours, wind.iloc[120:144]*wind_cap_install, pv.iloc[120:144]*pv_cap_install, bioenergy, hard_coal, lignite, natural_gas, oil, waste, discharge[120:144], hydro_discharge[120:144], charge[120:144], hydro_charge[120:144], colors=sns.color_palette("Set3"))
plt.legend(['Wind', 'PV', 'Bioenergy', 'Hard Coal', 'Lignite', 'Natural Gas', 'Oil', 'Waste', 'BESS Discharge', 'Hydro Discharge', 'BESS Charge', 'Hydro Charge'], loc='upper right')
plt.plot(hours, load[120:144], c='black')
plt.title('Hourly Dispatch over Day in Winter')
plt.ylabel('Generation/ Loads [MWh]')
plt.xlabel('Time [h]')
plt.savefig('Hourly Dispatch over Day in Winter')

# Plotting results for winter week
hours = np.arange(0, 168)
plt.figure(figsize=(10, 6))
plt.stackplot(hours, wind.iloc[120:288]*wind_cap_install, pv.iloc[120:288]*pv_cap_install, bioenergy_ww, hard_coal_ww, lignite_ww, natural_gas_ww, oil_ww, waste_ww, discharge[120:288], hydro_discharge[120:288], charge[120:288], hydro_charge[120:288], colors=sns.color_palette("Set3"))
plt.legend(['Wind', 'PV', 'Bioenergy', 'Hard Coal', 'Lignite', 'Natural Gas', 'Oil', 'Waste', 'BESS Discharge', 'Hydro Discharge', 'BESS Charge', 'Hydro Charge'], loc='upper right')
plt.plot(hours, load[120:288], c='black')
plt.title('Hourly Dispatch over Week in Winter')
plt.ylabel('Generation/ Loads [MWh]')
plt.xlabel('Time [h]')
plt.savefig('Hourly Dispatch over Week in Winter')

# Plotting results for summer week (indices adjusted)
hours = np.arange(0, 168)
plt.figure(figsize=(10, 6))
plt.stackplot(hours, wind.iloc[4000:4168]*wind_cap_install, pv.iloc[4000:4168]*pv_cap_install, bioenergy_sw, hard_coal_sw, lignite_sw, natural_gas_sw, oil_sw, waste_sw, discharge[4000:4168], hydro_discharge[4000:4168], charge[4000:4168], hydro_charge[4000:4168], colors=sns.color_palette("Set3"))
plt.legend(['Wind', 'PV', 'Bioenergy', 'Hard Coal', 'Lignite', 'Natural Gas', 'Oil', 'Waste', 'BESS Discharge', 'Hydro Discharge', 'BESS Charge', 'Hydro Charge'], loc='upper right')
plt.plot(hours, load[4000:4168], c='black')
plt.title('Hourly Dispatch over Week in Summer')
plt.ylabel('Generation/ Loads [MWh]')
plt.xlabel('Time [h]')
plt.savefig('Hourly Dispatch over Week in Summer')

# Geographic plotting for north and south Germany
ger_pp['zone'] = 'North'
ger_pp.loc[ger_pp['NUTS_NAME'].isin(nuts_name_sued), 'zone'] = 'South'
north = ger_pp.loc[ger_pp['zone'] == 'North']
south = ger_pp.loc[ger_pp['zone'] == 'South']

fig = plt.figure(figsize=(5, 10))
ax = plt.axes(projection=ccrs.epsg(3035))
nuts1.plot(ax=ax, edgecolor="black", facecolor="lightgrey")
north.to_crs(3035).plot(ax=ax, column="Fueltype", markersize=gdf.Capacity / 20, legend=True)
ax.set_title('Conventional Power Plants North Germany')
ax.set_extent([5, 19, 47, 55])
fig.savefig('Conventional Power Plants North Germany')

fig = plt.figure(figsize=(5, 10))
ax = plt.axes(projection=ccrs.epsg(3035))
nuts1.plot(ax=ax, edgecolor="black", facecolor="lightgrey")
south.to_crs(3035).plot(ax=ax, column="Fueltype", markersize=gdf.Capacity / 20, legend=True)
ax.set_title('Conventional Power Plants South Germany')
ax.set_extent([5, 19, 47, 55])
fig.savefig('Conventional Power Plants South Germany')
