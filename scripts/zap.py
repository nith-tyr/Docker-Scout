import json
import requests
import os

# Environment Variables
INFLUX_URL = os.getenv("INFLUX_URL")  # Example: http://your-influxdb-host:8086/api/v2/write
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

def parse_zap_json_to_line_protocol(file_path):
    try:
        with open(file_path, 'r') as f:
            zap_data = json.load(f)

        line_protocol_data = []

        # Iterate over vulnerabilities in the JSON report
        for site in zap_data.get("site", []):
            for alert in site.get("alerts", []):
                # Extract relevant fields
                risk = alert.get("risk", "Unknown")
                name = alert.get("name", "Unknown")
                description = alert.get("description", "No description")
                url = alert.get("url", "No URL")

                # Convert to line protocol
                line = f'zap_scan,risk={risk} name="{name}",description="{description}",url="{url}"'
                line_protocol_data.append(line)

        return "\n".join(line_protocol_data)

    except Exception as e:
        print(f"Error parsing ZAP JSON: {e}")
        return None

def send_to_influxdb(line_protocol_data):
    try:
        headers = {
            "Authorization": f"Token {INFLUX_TOKEN}",
            "Content-Type": "text/plain",
        }
        params = {
            "org": INFLUX_ORG,
            "bucket": INFLUX_BUCKET,
            "precision": "s",
        }

        response = requests.post(INFLUX_URL, headers=headers, params=params, data=line_protocol_data)

        if response.status_code == 204:
            print("Data sent successfully to InfluxDB!")
        else:
            print(f"Failed to send data to InfluxDB: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error sending data to InfluxDB: {e}")

if __name__ == "__main__":
    # Path to the ZAP JSON report
    zap_json_file = "report_json.json"

    if not os.path.exists(zap_json_file):
        print(f"Error: ZAP JSON report not found at {zap_json_file}")
        exit(1)

    # Parse JSON and convert to line protocol
    line_protocol_data = parse_zap_json_to_line_protocol(zap_json_file)
    if line_protocol_data:
        # Send to InfluxDB
        send_to_influxdb(line_protocol_data)
