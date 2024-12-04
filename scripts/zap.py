import os
import json
import requests


def process_zap_metrics(file_path):
    """
    Reads ZAP scan report, processes metrics, and sends them to InfluxDB.

    Args:
        file_path (str): Path to the ZAP JSON report.
    """
    # InfluxDB connection details from environment variables
    influx_url = os.getenv("INFLUX_URL")
    org = os.getenv("INFLUX_ORG")
    bucket = os.getenv("INFLUX_BUCKET")
    token = os.getenv("INFLUX_TOKEN")

    if not all([influx_url, org, bucket, token]):
        raise ValueError("InfluxDB connection details are not set in environment variables.")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "text/plain"
    }

    # Verify the ZAP JSON file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ZAP scan report not found: {file_path}")

    # Read the ZAP scan report
    with open(file_path, "r") as file:
        zap_data = json.load(file)

    # Process the ZAP scan metrics
    lines = []
    for alert in zap_data.get("site", []):
        for issue in alert.get("alerts", []):
            metric = issue.get("alert", "unknown")
            risk = issue.get("risk", "unknown")
            count = len(issue.get("instances", []))
            lines.append(f"{metric},risk={risk} count={count}")

    # Send data to InfluxDB
    influx_write_url = f"{influx_url}/api/v2/write?org={org}&bucket={bucket}&precision=s"
    response = requests.post(
        influx_write_url,
        data="\n".join(lines),
        headers=headers
    )

    if response.status_code == 204:
        print("ZAP scan report sent successfully to InfluxDB!")
    else:
        print(f"Failed to send data: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Path to the ZAP scan report
    zap_report_path = "zap_reports/report_json.json"

    # Process and send the metrics
    process_zap_metrics(zap_report_path)
