import json
import pdfkit
import sys
import os

def main(sarif_file):
    # Load SARIF data
    with open(sarif_file, "r") as f:
        sarif_data = json.load(f)

    # Convert SARIF to HTML
    html_content = f"""
    <html>
    <head><title>Docker Scout Report</title></head>
    <body>
    <h1>Docker Scout Analysis</h1>
    <pre>{json.dumps(sarif_data, indent=4)}</pre>
    </body>
    </html>
    """

    # Save HTML to a file
    with open("scout-report.html", "w") as f:
        f.write(html_content)

    # Convert HTML to PDF
    pdfkit.from_file("scout-report.html", "scout-report.pdf")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_pdf.py <sarif_file>")
        sys.exit(1)
    
    sarif_file = sys.argv[1]
    main(sarif_file)
