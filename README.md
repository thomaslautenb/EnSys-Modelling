
# EnSys-Modelling

EnSys-Modelling is a Python-based framework for energy system modeling and optimization. This project leverages Pyomo for defining and solving optimization models, and it includes comprehensive data preparation and analysis for energy generation and storage systems.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Data Preparation](#data-preparation)
- [Optimization Model](#optimization-model)
- [Execution](#execution)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this project, you need to have Python installed along with the following packages:
- numpy
- pandas
- matplotlib
- seaborn
- pyomo
- cartopy

You can install these dependencies using pip:
```bash
pip install numpy pandas matplotlib seaborn pyomo cartopy
```

## Project Structure

The project structure is organized as follows:
```
EnSys-Modelling/
├── data_preparation.py
├── model.py
├── execute_model.py
├── data/
│   ├── capacities_federal_states.csv
│   ├── efficiencies_federal_states.csv
│   ├── mc_federal_states.csv
│   ├── co2_federal_states.csv
│   ├── ger_pp.csv
│   ├── nuts1.csv
│   ├── wind.csv
│   ├── pv.csv
│   ├── load.csv
│   ├── charge.csv
│   ├── discharge.csv
│   ├── hydro_charge.csv
│   └── hydro_discharge.csv
├── results/
│   ├── dispatch_day_winter.csv
│   ├── dispatch_day_summer.csv
│   ├── dispatch_week_winter.csv
│   ├── dispatch_week_summer.csv
│   ├── Hourly_Dispatch_Day_Winter.png
│   ├── Hourly_Dispatch_Week_Winter.png
│   ├── Hourly_Dispatch_Week_Summer.png
│   ├── Conventional_Power_Plants_North_Germany.png
│   └── Conventional_Power_Plants_South_Germany.png
└── README.md
```

## Usage

1. **Data Preparation**: Run the data preparation script to load and prepare the necessary datasets.
2. **Model Definition**: Define the optimization model using the prepared data.
3. **Execution**: Execute the model and generate results for analysis.

### Data Preparation

The data preparation script (`data_preparation.py`) handles loading and processing the input data. It reads the CSV files, fills missing values, and aggregates the data as needed.

To run the data preparation:
```bash
python data_preparation.py
```

### Optimization Model

The model definition script (`model.py`) creates and solves the optimization model using Pyomo. It includes constraints for generation capacities, battery storage, and pumped hydro storage.

### Execution

The execution script (`execute_model.py`) runs the entire process, from data loading to model solving and result generation. It produces visualizations for energy dispatch over specific periods.

To execute the model:
```bash
python execute_model.py
```

## Results

The results are saved in the `results/` directory, including CSV files with dispatch data and visualizations of the energy system's performance.

## Report
### Abstract
This project aims to develop an integrated energy system model to optimize the generation and storage of renewable energy sources. The model includes various types of power plants, battery energy storage systems (BESS), and pumped hydro storage. The optimization framework is designed to minimize the total operational cost while meeting the energy demand and adhering to the capacity constraints of different energy sources. The results provide insights into the optimal dispatch of energy resources over different periods, such as winter and summer weeks, highlighting the system's flexibility and reliability.

The complete report can be found under report.


