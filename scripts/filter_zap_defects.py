import json
import sys

def filter_defects(input_file, output_file, severities):
    with open(input_file, 'r') as f:
        zap_results = json.load(f)

    filtered_results = {
        "site": []
    }

    # Iterate over the sites and filter the alerts by severity
    for site in zap_results.get('site', []):
        filtered_site = {"alerts": []}
        for alert in site.get('alerts', []):
            if alert['risk'] in severities:
                filtered_site['alerts'].append(alert)
        if filtered_site['alerts']:
            filtered_results['site'].append(filtered_site)

    # Write the filtered results to the output file
    with open(output_file, 'w') as f:
        json.dump(filtered_results, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_zap_defects.py <input_file> <output_file>")
        sys.exit(1)

    # Call the filtering function with Low and High severities
    filter_defects(
        input_file=sys.argv[1],
        output_file=sys.argv[2],
        severities=["Low", "High"]
    )
