# test_synthetic_data.py

# Import the necessary functions from your anomaly detector script
from layer1 import load_rules_from_csv, detect_layer1  
from typing import Dict, Any, List
def generate_synthetic_data():
    """Generates a list of synthetic sensor readings for testing purposes."""
    data = [
        # --- Normal (Healthy) Readings ---
        {
            "test_case": "Tropical - Normal Monsoon Reading",
            "data": {"timestamp": "2025-07-22T10:00:00", "region": "tropical", "soil_moisture": 30, "soil_temperature": 29, "ph": 6.0, "ec": 1.5, "n": 40, "p": 30, "k": 200, "co2_flux": 150}
        },
        {
            "test_case": "Temperate - Normal Summer Reading",
            "data": {"timestamp": "2025-07-22T10:00:00", "region": "temperate", "soil_moisture": 25, "soil_temperature": 22, "ph": 6.8, "ec": 1.2, "n": 30, "p": 25, "k": 180, "co2_flux": 100}
        },
        {
            "test_case": "Arid - Normal Irrigation Season Reading",
            "data": {"timestamp": "2025-07-22T10:00:00", "region": "arid_semi_arid", "soil_moisture": 20, "soil_temperature": 33, "ph": 7.5, "ec": 2.5, "n": 25, "p": 20, "k": 200, "co2_flux": 40}
        },
        
        # --- Point Anomaly Tests ---
        {
            "test_case": "Tropical - Critically High Moisture (Point)",
            "data": {"timestamp": "2025-04-10T12:00:00", "region": "tropical", "soil_moisture": 65, "soil_temperature": 30}
        },
        {
            "test_case": "Temperate - Critically Low Temperature (Point)",
            "data": {"timestamp": "2025-11-05T22:00:00", "region": "temperate", "soil_moisture": 30, "soil_temperature": 4}
        },
        {
            "test_case": "Arid - Critically High pH (Point)",
            "data": {"timestamp": "2025-08-15T14:00:00", "region": "arid_semi_arid", "soil_moisture": 20, "soil_temperature": 35, "ph": 9.7}
        },

        # --- Contextual Anomaly Tests ---
        {
            "test_case": "Tropical - Dry for Monsoon Season (Contextual)",
            "data": {"timestamp": "2025-08-01T11:00:00", "region": "tropical", "soil_moisture": 13, "soil_temperature": 30}
        },
        {
            "test_case": "Temperate - Too Cold for Spring Planting (Contextual)",
            "data": {"timestamp": "2025-04-15T08:00:00", "region": "temperate", "soil_moisture": 25, "soil_temperature": 6}
        },
        {
            "test_case": "Arid - High Salinity during Dry Season (Contextual)",
            "data": {"timestamp": "2025-01-20T15:00:00", "region": "arid_semi_arid", "soil_moisture": 15, "soil_temperature": 18, "ec": 5.5}
        },
        {
            "test_case": "Tropical - Night Temperature Too High (Contextual)",
            "data": {"timestamp": "2025-06-25T02:00:00", "region": "tropical", "soil_moisture": 40, "soil_temperature": 34}
        },

        # --- Error Handling Tests ---
        {
            "test_case": "Invalid Region",
            "data": {"timestamp": "2025-07-22T10:00:00", "region": "arctic", "soil_moisture": 50}
        },
        {
            "test_case": "Missing Timestamp",
            "data": {"region": "temperate", "soil_moisture": 25}
        }
    ]
    return data

if __name__ == "__main__":
    # 1. Load rules from the CSV file
    rules_file = 'soil_rules.csv'
    loaded_rules = load_rules_from_csv(rules_file)

    if not loaded_rules:
        print("Testing aborted because rules could not be loaded.")
    else:
        print(f"✅ Rules successfully loaded. Starting synthetic data tests...\n")
        
        # 2. Get synthetic data
        synthetic_data = generate_synthetic_data()
        
        # 3. Process each test case
        for item in synthetic_data:
            test_case_name = item["test_case"]
            reading = item["data"]
            
            print(f"--- Running Test Case: {test_case_name} ---")
            print(f"Input: {reading}")
            
            anomalies_found = detect_layer1(reading, loaded_rules)
            
            if anomalies_found:
                print(f"✅ Result: Anomalies Detected ({len(anomalies_found)})")
                for anomaly in anomalies_found:
                    print(f"  - {anomaly}")
            else:
                print("✅ Result: No anomalies detected.")
            print("-" * 50 + "\n")