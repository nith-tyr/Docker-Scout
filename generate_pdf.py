import json
import pdfkit
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main(github_url):
    # Configure Selenium to use Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless to avoid UI issues
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to GitHub Actions artifact page
    driver.get(github_url)

    # Locate the SARIF artifact link and click to download
    artifact_link = driver.find_element(By.LINK_TEXT, "docker-scout-sarif")
    artifact_link.click()

    # Define the expected download path
    download_path = os.path.expanduser("~/Downloads/sarif.output.json")
    driver.quit()

    # Load SARIF data
    with open(download_path, "r") as f:
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
    # Get GitHub URL from command line arguments
    if len(sys.argv) != 2:
        print("Usage: python generate_pdf.py <github_url>")
        sys.exit(1)
    
    github_url = sys.argv[1]
    main(github_url)
