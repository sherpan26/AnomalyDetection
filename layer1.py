import pandas as pd
import datetime
from typing import Dict, List, Any

def load_rules_from_csv(filepath: str) -> Dict:
    """
    Loads and parses the anomaly detection rules from a specified CSV file.

    Args:
        filepath: The path to the CSV file containing the rules.

    Returns:
        A nested dictionary of rules compatible with the detection function.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: The rule file was not found at '{filepath}'")
        return {}

    rules_dict = {}
    # Replace NaN with None for easier processing
    df = df.where(pd.notna(df), None)

    for _, row in df.iterrows():
        region = row['region']
        param = row['parameter']
        rule_type = row['rule_type']

        # Ensure region and parameter keys exist
        if region not in rules_dict:
            rules_dict[region] = {}
        if param not in rules_dict[region]:
            rules_dict[region][param] = {}

        if rule_type == 'point':
            rules_dict[region][param]['point'] = {
                "low": row['low_threshold'],
                "high": row['high_threshold'],
                "message_low": row['message_low'],
                "message_high": row['message_high']
            }
        elif rule_type == 'contextual':
            if 'contextual' not in rules_dict[region][param]:
                rules_dict[region][param]['contextual'] = []
            
            context_rule = {
                "name": row['context_name'],
                "low": row['low_threshold'],
                "high": row['high_threshold'],
                "message_low": row['message_low'],
                "message_high": row['message_high']
            }
            if row['months']:
                context_rule['months'] = [int(m) for m in str(row['months']).split(',')]
            if row['hours']:
                context_rule['hours'] = [int(h) for h in str(row['hours']).split(',')]
            
            rules_dict[region][param]['contextual'].append(context_rule)
            
    return rules_dict

def detect_layer1(sensor_reading: Dict[str, Any], rules: Dict) -> List[Dict[str, Any]]:
    """
    Detects anomalies in a sensor reading using a rule-based filter.

    Args:
        sensor_reading: A dictionary containing the sensor data.
        rules: A dictionary of loaded rules to apply.

    Returns:
        A list of dictionaries, where each represents a detected anomaly.
    """
    anomalies = []
    
    try:
        dt = datetime.datetime.fromisoformat(sensor_reading["timestamp"])
        month = dt.month
        hour = dt.hour
        region = sensor_reading["region"]
    except (KeyError, ValueError) as e:
        anomalies.append({"parameter": "metadata", "value": str(sensor_reading), "type": "error", "context": None, "message": f"Invalid sensor reading format: {e}"})
        return anomalies

    if region not in rules:
        anomalies.append({"parameter": "region", "value": region, "type": "error", "context": None, "message": f"Region '{region}' not found in rules database."})
        return anomalies

    region_rules = rules.get(region, {})

    for param, param_rules in region_rules.items():
        if param not in sensor_reading or sensor_reading[param] is None:
            continue

        value = sensor_reading[param]
        
        # Check for Point Anomalies
        point_rules = param_rules.get("point")
        if point_rules:
            if point_rules.get("low") is not None and value < point_rules["low"]:
                anomalies.append({"parameter": param, "value": value, "type": "point", "context": None, "message": point_rules.get("message_low")})
            elif point_rules.get("high") is not None and value > point_rules["high"]:
                 anomalies.append({"parameter": param, "value": value, "type": "point", "context": None, "message": point_rules.get("message_high")})

        # Check for Contextual Anomalies
        contextual_rules = param_rules.get("contextual", [])
        for rule in contextual_rules:
            month_match = "months" in rule and month in rule["months"]
            hour_match = "hours" in rule and hour in rule["hours"]
            
            if month_match or hour_match:
                if rule.get("low") is not None and value < rule["low"]:
                    anomalies.append({"parameter": param, "value": value, "type": "contextual", "context": rule["name"], "message": rule.get("message_low")})
                elif rule.get("high") is not None and value > rule["high"]:
                    anomalies.append({"parameter": param, "value": value, "type": "contextual", "context": rule["name"], "message": rule.get("message_high")})

    return anomalies

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Load rules from the CSV file
    rules_file = 'soil_rules.csv'
    loaded_rules = load_rules_from_csv(rules_file)

    if loaded_rules:
        print(f"✅ Rules successfully loaded from '{rules_file}'.\n")
        
        # 2. Define sample data to test
        sample_data = [
            # Tropical, Monsoon season, critically low moisture (Point Anomaly)
            {"timestamp": "2025-07-18T12:00:00", "region": "tropical", "soil_moisture": 6.5, "soil_temperature": 28},
            # Temperate, Winter, road salt contamination (Contextual Anomaly)
            {"timestamp": "2025-01-20T11:00:00", "region": "temperate", "soil_moisture": 30, "soil_temperature": 1, "ec": 3.7},
            # Arid, Dry Season, multiple anomalies
            {"timestamp": "2025-12-22T08:00:00", "region": "arid_semi_arid", "soil_moisture": 2.5, "soil_temperature": 48, "ph": 9.8}
        ]

        # 3. Process the data
        for i, reading in enumerate(sample_data):
            print(f"--- Checking Sample Reading #{i+1} ---")
            print(f"Input: {reading}")
            anomalies_found = detect_layer1(reading, loaded_rules)
            if anomalies_found:
                print(f"Anomalies Detected ({len(anomalies_found)}):")
                for anomaly in anomalies_found:
                    print(f"  - {anomaly}")
            else:
                print("No anomalies detected.")
            print("-" * 40 + "\n")
        