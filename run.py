import pandas as pd
from collections import deque
# Assume your functions are in these files:
from layer1 import load_rules_from_csv, detect_layer1
from layer2 import detect_layer2

# --- CONFIGURATION ---
RULES_FILE = 'soil_rules.csv'
DATA_FILE = 'prepared_data.csv' # Using the longer test data
WINDOW_SIZE = 5
Z_THRESHOLD = 3.0

# --- SCRIPT LOGIC ---
# 1. Load rules and data
rules = load_rules_from_csv(RULES_FILE)
df = pd.read_csv(DATA_FILE)

# 2. Use a deque for an efficient sliding window
historical_data = deque(maxlen=WINDOW_SIZE)

print("Processing data with new reinforcement logic...\n")

# 3. Process data row by row
for index, row in df.iterrows():
    print(f"--- Processing row index: {index} ---")
    current_reading = row.to_dict()
    
    # This list will hold only the anomalies that pass the new logic
    final_anomalies_to_report = []

    # --- Run Layer 1 First ---
    anomalies_l1 = detect_layer1(current_reading, rules)

    # --- NEW CONDITIONAL LOGIC BASED ON SUJIT'S REQUEST ---
    if anomalies_l1:
        # Separate L1 anomalies by type
        point_anomalies_l1 = [anom for anom in anomalies_l1 if anom['type'] == 'point']
        contextual_anomalies_l1 = [anom for anom in anomalies_l1 if anom['type'] == 'contextual']

        # 1. Handle Contextual Anomalies: Report them directly and ignore Layer 2
        if contextual_anomalies_l1:
            final_anomalies_to_report.extend(contextual_anomalies_l1)

        # 2. Handle Point Anomalies: Check for reinforcement from Layer 2 (AND logic)
        if point_anomalies_l1 and len(historical_data) == WINDOW_SIZE:
            anomalies_l2 = detect_layer2(current_reading, list(historical_data), WINDOW_SIZE, Z_THRESHOLD)
            
            if anomalies_l2:
                # Get the set of parameters that Layer 2 flagged as statistical anomalies
                l2_flagged_params = {anom['parameter'] for anom in anomalies_l2}

                # Find the L1 point anomalies that are on the SAME parameter as an L2 anomaly
                for l1_anom in point_anomalies_l1:
                    if l1_anom['parameter'] in l2_flagged_params:
                        # This is a reinforced anomaly, add it to the final report
                        l1_anom['message'] += " (Reinforced by Layer 2)"
                        final_anomalies_to_report.append(l1_anom)

    # --- Report Final Anomalies ---
    if final_anomalies_to_report:
        print("Anomalies Found:")
        for anom in final_anomalies_to_report:
            print(f"  - {anom}")
            
    # Add the current reading to the history for the next iteration's Layer 2 check
    historical_data.append(current_reading)
    print("-" * 40 + "\n")