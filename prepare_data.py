import pandas as pd

# --- CONFIGURATION ---
original_file = 'simulated_soil_sensor_data_with_anomalies(1).csv'
new_file = 'prepared_data.csv'

print(f"Loading original data from '{original_file}'...")
# Load the dataset
try:
    df = pd.read_csv(original_file)
except FileNotFoundError:
    print(f"Error: The file '{original_file}' was not found. Please make sure it's in the same directory.")
    exit()

# --- DATA TRANSFORMATION ---

# 1. Define the mapping from old column names to new ones
column_mapping = {
    'Timestamp': 'timestamp',
    'Moisture_VWC_%': 'soil_moisture',
    'Temperature_C': 'soil_temperature',
    'pH': 'ph',
    'EC_dS_m': 'ec',
    'Nitrogen_ppm': 'n',
    'Phosphorous_ppm': 'p',
    'Potassium_ppm': 'k',
    'CO2_ppm': 'co2_flux' # Note: We are keeping this column, but the units differ from the rules
}

# 2. Rename the columns
df.rename(columns=column_mapping, inplace=True)
print("Columns successfully renamed.")

# 3. Add the required 'region' column
df['region'] = 'temperate'
print("Added 'region' column with value 'temperate'.")

# 4. Save the prepared data to a new CSV file
df.to_csv(new_file, index=False)
print(f"\n✅ Success! The prepared data has been saved to '{new_file}'.")