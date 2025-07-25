import pandas as pd
from collections import deque
# Assume your functions are in these files:
from layer1 import load_rules_from_csv, detect_layer1
from layer2 import detect_layer2

# --- CONFIGURATION ---
RULES_FILE = 'soil_rules.csv'
DATA_FILE = 'test1_data.csv'
WINDOW_SIZE = 5 # Should match the number of "Pre-Spike" rows
Z_THRESHOLD = 3.0

# --- SCRIPT LOGIC ---
# 1. Load rules and data
rules = load_rules_from_csv(RULES_FILE)
df = pd.read_csv(DATA_FILE)

# 2. Use a deque for an efficient sliding window
historical_data = deque(maxlen=WINDOW_SIZE)

# 3. Process data row by row
for index, row in df.iterrows():
    print(f"--- Processing: {row['test_case']} ---")
    current_reading = row.to_dict()
    
    # --- Run Layer 1 ---
    anomalies_l1 = detect_layer1(current_reading, rules)
    if anomalies_l1:
        print("Layer 1 Anomalies Found:")
        for anom in anomalies_l1:
            print(f"  - {anom}")

    # --- Run Layer 2 ---
    # Only run if the window is full
    if len(historical_data) == WINDOW_SIZE:
        anomalies_l2 = detect_layer2(current_reading, list(historical_data), WINDOW_SIZE, Z_THRESHOLD)
        if anomalies_l2:
            print("Layer 2 Anomalies Found:")
            for anom in anomalies_l2:
                print(f"  - {anom}")
    
    # Add the current reading to the history for the next iteration
    historical_data.append(current_reading)
    print("-" * 40 + "\n")