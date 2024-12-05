import json
import os
import requests

def send_json_to_influxdb(json_file):
    try:
        # Load the JSON data
        with open(json_file) as f:
            data = json.load(f)

        # Extract and format data for InfluxDB (adjust according to your JSON structure)
        measurements = []
        for alert in data.get("alerts", []):
            measurement = "zap_alerts"
            tags = f"severity={alert['riskLevel']},alert_id={alert['alertRef']}"
            fields = f"description=\"{alert['description']}\""
            line_protocol = f"{measurement},{tags} {fields}"
            measurements.append(line_protocol)

        # Send data to InfluxDB
        influx_url = os.getenv('INFLUX_URL')
        influx_token = os.getenv('INFLUX_TOKEN')
        influx_org = os.getenv('INFLUX_ORG')
        influx_bucket = os.getenv('INFLUX_BUCKET')

        if not influx_url or not influx_token or not influx_org or not influx_bucket:
            print("InfluxDB configuration missing")
            return

        url = f"{influx_url}/api/v2/write?org={influx_org}&bucket={influx_bucket}&precision=s"
        headers = {
            "Authorization": f"Token {influx_token}",
            "Content-Type": "text/plain"
        }
        data_payload = "\n".join(measurements)

        response = requests.post(url, headers=headers, data=data_payload)
        if response.status_code != 204:
            print(f"Failed to send data to InfluxDB: {response.status_code} - {response.text}")
        else:
            print("Data successfully sent to InfluxDB")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    json_file_path = "zap_reports/report_json.json"  # Path to your JSON file
    send_json_to_influxdb(json_file_path)
