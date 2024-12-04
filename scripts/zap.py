import json
import os
import requests

def send_zap_report_to_influxdb(report_file):
    # Load the ZAP JSON report
    try:
        with open(report_file) as f:
            zap_data = json.load(f)
    except Exception as e:
        print(f"Error loading ZAP report: {e}")
        return
    
    # Example: Extracting a few fields (adapt this to your actual data structure)
    measurements = []
    for item in zap_data.get('alerts', []):
        # Measurement name (influxdb line protocol)
        measurement = 'zap_alerts'

        # Tags (metadata - you can customize this based on your needs)
        tags = f"alert_id={item['alertRef']},severity={item['riskLevel']}"

        # Fields (the actual values you want to store)
        fields = f"message=\"{item['description']}\",timestamp={item['timestamp']}"

        # Combine into InfluxDB line protocol format
        line_protocol = f"{measurement},{tags} {fields}"
        measurements.append(line_protocol)

    # Send data to InfluxDB
    influx_url = os.getenv('INFLUX_URL')
    influx_token = os.getenv('INFLUX_TOKEN')
    influx_org = os.getenv('INFLUX_ORG')
    influx_bucket = os.getenv('INFLUX_BUCKET')

    if not influx_url or not influx_token or not influx_org or not influx_bucket:
        print("Missing InfluxDB environment variables")
        return

    url = f'{influx_url}/api/v2/write?org={influx_org}&bucket={influx_bucket}&precision=s'
    headers = {
        'Authorization': f'Token {influx_token}',
        'Content-Type': 'text/plain',
    }

    # Combine all measurements into a single payload
    data = '\n'.join(measurements)

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 204:
            print(f"Failed to send data to InfluxDB: {response.status_code} - {response.text}")
        else:
            print("Data successfully sent to InfluxDB")
    except Exception as e:
        print(f"Error sending data to InfluxDB: {e}")


if __name__ == "__main__":
    report_file = 'zap_reports/report_json.json'  # Path to the ZAP JSON report
    send_zap_report_to_influxdb(report_file)
