# layer2.py
import numpy as np
from typing import Dict, List, Any

def detect_layer2(
    current_reading: Dict[str, Any],
    historical_data: List[Dict[str, Any]],
    window_size: int,
    z_score_threshold: float = 3.0
) -> List[Dict[str, Any]]:
    """
    Detects statistical anomalies using a Z-score over a sliding window.

    This function compares a current sensor reading to the mean and standard
    deviation of its recent history to find values that are statistically
    unlikely.

    Args:
        current_reading: The single, most recent sensor reading.
        historical_data: A list of recent sensor readings preceding the current one.
        window_size: The number of historical data points to consider for the baseline.
        z_score_threshold: The number of standard deviations from the mean to be
                           considered an anomaly. A common value is 2 or 3.

    Returns:
        A list of dictionaries, where each dictionary represents a detected
        statistical anomaly. Returns an empty list if no anomalies are found.
    """
    anomalies = []
    
    # Exit early if there isn't enough historical data to analyze.
    if len(historical_data) < window_size:
        return anomalies

    # Define the parameters to check for statistical anomalies.
    params_to_check = [
        'soil_moisture', 'soil_temperature', 'ph', 'ec',
        'n', 'p', 'k', 'co2_flux'
    ]

    for param in params_to_check:
        if param not in current_reading or current_reading[param] is None:
            continue

        # Create a list of historical values for the current parameter.
        history_values = [
            rec[param] for rec in historical_data if param in rec and rec[param] is not None
        ]
        
        # Ensure we have enough valid data points for a meaningful calculation.
        if len(history_values) < window_size:
            continue
        
        # Calculate mean and standard deviation from the historical window.
        mean = np.mean(history_values)
        std_dev = np.std(history_values)
        current_value = current_reading[param]

        # Handle the edge case where standard deviation is zero.
        if std_dev == 0:
            # If all historical values are the same, any different value is an anomaly.
            if current_value != mean:
                z_score = float('inf')
            else:
                z_score = 0.0
        else:
            z_score = (current_value - mean) / std_dev

        # Check if the absolute Z-score exceeds the defined threshold.
        if abs(z_score) > z_score_threshold:
            anomalies.append({
                "parameter": param,
                "value": current_value,
                "type": "statistical",
                "context": f"Z-score of {z_score:.2f} exceeds threshold ({z_score_threshold}). "
                           f"Value is {abs(z_score):.2f} std deviations from the {window_size}-reading average of {mean:.2f}."
            })
            
    return anomalies

# --- Example Usage ---
# This block demonstrates how the function works if you run this file directly.
if __name__ == "__main__":
    # 1. Create a sample history of 10 stable readings.
    historical_readings = [
        {'soil_moisture': 35.1, 'soil_temperature': 22.5},
        {'soil_moisture': 35.3, 'soil_temperature': 22.5},
        {'soil_moisture': 35.2, 'soil_temperature': 22.6},
        {'soil_moisture': 35.4, 'soil_temperature': 22.5},
        {'soil_moisture': 35.3, 'soil_temperature': 22.6},
        {'soil_moisture': 35.5, 'soil_temperature': 22.7},
        {'soil_moisture': 35.4, 'soil_temperature': 22.6},
        {'soil_moisture': 35.6, 'soil_temperature': 22.7},
        {'soil_moisture': 35.5, 'soil_temperature': 22.8},
        {'soil_moisture': 35.7, 'soil_temperature': 22.7},
    ]

    # 2. Define a new reading with a sudden, sharp drop in moisture.
    current_reading_anomaly = {'soil_moisture': 25.0, 'soil_temperature': 22.7}
    
    # 3. Define a new reading that follows the recent pattern.
    current_reading_normal = {'soil_moisture': 35.8, 'soil_temperature': 22.8}

    # --- Run the detection ---
    WINDOW = 10
    Z_THRESHOLD = 3.0
    
    print(f"--- Testing for a statistical anomaly (sudden drop) ---")
    statistical_anomalies = detect_layer2(
        current_reading_anomaly,
        historical_readings,
        window_size=WINDOW,
        z_score_threshold=Z_THRESHOLD
    )

    if statistical_anomalies:
        print("✅ Statistical Anomaly Detected:")
        for anom in statistical_anomalies:
            print(f"  - {anom}")
    else:
        print("No statistical anomalies detected.")
        
    print("\n" + "-"*50 + "\n")

    print(f"--- Testing a normal reading ---")
    normal_run = detect_layer2(
        current_reading_normal,
        historical_readings,
        window_size=WINDOW,
        z_score_threshold=Z_THRESHOLD
    )
    
    if normal_run:
        print("Anomaly Detected:")
        for anom in normal_run:
            print(f"  - {anom}")
    else:
        print("✅ No statistical anomalies detected.")