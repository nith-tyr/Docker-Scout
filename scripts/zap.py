# convert_json_to_line_protocol.py
import json
import time

def json_to_line_protocol(json_file, measurement, output_file):
    """
    Converts a JSON file into InfluxDB line protocol format.

    Args:
        json_file (str): Path to the input JSON file.
        measurement (str): Measurement name for the line protocol.
        output_file (str): Path where the output line protocol will be written.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create a list to store line protocol entries
    line_protocol = []

    # Loop through the JSON data (assuming it's a list of reports or records)
    for item in data:
        # Example assumption on the JSON structure (modify as per your structure)
        tags = f"report_id={item.get('id', 'N/A')},type={item.get('type', 'N/A')}"
        fields = f"value={item.get('value', 0)}"
        timestamp = int(time.time() * 1e9)  # Current time in nanoseconds
        
        # Construct line protocol entry
        line = f"{measurement},{tags} {fields} {timestamp}"
        line_protocol.append(line)

    # Write the line protocol to the output file
    with open(output_file, 'w') as f:
        f.write("\n".join(line_protocol))
    print(f"Line protocol written to {output_file}")

# Run the function with the specified parameters
if __name__ == "__main__":
    json_to_line_protocol('zap_reports/report_json.json', 'zap_report', 'zap_reports/zap_report.lp')
