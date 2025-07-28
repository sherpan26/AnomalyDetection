Soil Anomaly Detection System
This project implements a sophisticated two-layer anomaly detection system for agricultural soil sensor data. It is designed to identify and flag a wide range of abnormalities, from critical threshold breaches to subtle statistical deviations, providing a comprehensive assessment of soil health conditions.

System Architecture
The system uses a multi-layered approach to analyze sensor data, ensuring both high sensitivity and high confidence in its findings. Each data point is processed sequentially through two distinct analytical layers.

Layer 1: Rule-Based Filter
This layer acts as the first line of defense, using a set of expert-defined rules to check for clear violations. It can detect both critical point anomalies (e.g., a dangerously low pH) and contextual anomalies that depend on the time of year or day (e.g., abnormally low moisture for the growing season).

Layer 2: Statistical Anomaly Engine
This layer looks for patterns and behaviors that are statistically unusual, even if no hard rules have been broken. It uses a Z-score algorithm over a sliding window of recent data to identify sudden spikes, gradual drifts, or any other significant deviation from the established norm.

Features
Modular Design: The logic is separated into distinct, single-responsibility Python scripts (layer1.py, layer2.py), making the system easy to understand, maintain, and scale.

Flexible Rule Management: All Layer 1 rules are managed in an external soil_rules.csv file, allowing for easy updates by domain experts without touching the core code.

Reinforced Anomaly Detection: Implements a high-confidence alerting system where critical point anomalies are only reported if they are "reinforced" (confirmed) by a statistical anomaly from Layer 2.

Comprehensive Data Handling: Includes scripts to prepare and clean raw data, ensuring it is in the correct format for analysis.

Robust Testing: Validated using multiple synthetic datasets designed to test various normal and anomalous scenarios.

File Structure
.
├── soil_rules.csv              # Contains all expert rules for Layer 1.
├── layer1.py                   # Implements the rule-based detection logic.
├── layer2.py                   # Implements the statistical (Z-score) detection logic.
├── prepare_data.py             # Script to clean and format raw data for analysis.
├── prepared_data.csv           # The clean, analysis-ready data file.
├── run.py                      # The main script to execute the full detection pipeline.
└── README.md                   # This documentation file.

How It Works
The main script, run.py, orchestrates the analysis by processing each row of the dataset according to the following logic:

Initial Check: Each sensor reading is first passed to Layer 1.

Logic Branching:

If a contextual anomaly is found, it is reported immediately, and the analysis for that data point stops.

If a point anomaly is found, the system proceeds to Layer 2 to seek confirmation.

If no anomaly is found by Layer 1, no alert is generated at this stage.

Reinforcement (AND Logic): A point anomaly from Layer 1 is only reported to the user if Layer 2 also flags the same parameter as a statistical anomaly. This ensures that reported critical events are both rule violations and significant statistical deviations.

This "reinforcement" model is designed to reduce noise and produce fewer, higher-confidence alerts for the most critical events.

Getting Started
Follow these steps to set up and run the project on your local machine.

Prerequisites

Python 3.x

pip (Python package installer)

Installation

Clone the repository:

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

Install the required Python libraries:

pip install pandas numpy

Running the System

Prepare the Data (if needed):
If you are using a new raw data file, place it in the project directory and run the preparation script.

python prepare_data.py

This will generate the prepared_data.csv file.

Execute the Anomaly Detection:
Run the main script to process the data and see the results.

python run.py

The output will be printed directly to your terminal.

Data
The system is designed to work with time-series data containing the following soil parameters:
timestamp, region, soil_moisture, soil_temperature, ph, ec, n, p, k, co2_flux.

The region column is used by Layer 1 to select the correct set of rules (temperate, tropical, or arid_semi_arid).

A sample prepared_data.csv file is included for demonstration and testing purposes.

Example Output
When you run the script, you will see a detailed log of the analysis. Here is a sample of what the output looks like when anomalies are detected:

--- Processing row index: 425 ---
Anomalies Found:
  - {'parameter': 'soil_moisture', 'value': 7.52, 'type': 'point', 'context': None, 'message': 'Permanent wilting point risk (Reinforced by Layer 2)'}
----------------------------------------

--- Processing row index: 335 ---
Anomalies Found:
  - {'parameter': 'co2_flux', 'value': 713.0, 'type': 'contextual', 'context': 'summer_peak', 'message': 'Bio-activity high for summer peak'}
  - {'parameter': 'co2_flux', 'value': 713.0, 'type': 'point', 'context': None, 'message': 'Excessive decomposition/stress (Reinforced by Layer 2)'}
----------------------------------------
