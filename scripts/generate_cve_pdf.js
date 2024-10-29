const AdmZip = require('adm-zip'); // For extracting ZIP files
const fs = require('fs');
const puppeteer = require('puppeteer');

// Path to the ZIP file and expected JSON file name
const zipFilePath = './sarif-results.zip'; // Adjust path as needed
const extractedJsonPath = './sarif-results.json';

// Step 1: Extract JSON from ZIP
function extractJsonFromZip(zipPath, outputJsonPath) {
  const zip = new AdmZip(zipPath);
  const zipEntries = zip.getEntries(); // Get all entries inside the ZIP

  // Search for the JSON file inside the ZIP
  const jsonEntry = zipEntries.find((entry) => entry.entryName.endsWith('.json'));
  if (!jsonEntry) {
    console.error('JSON file not found in the ZIP!');
    process.exit(1);
  }

  // Extract the JSON file to the output path
  fs.writeFileSync(outputJsonPath, jsonEntry.getData().toString('utf8'));
  console.log(`Extracted ${jsonEntry.entryName} to ${outputJsonPath}`);
}

// Step 2: Generate PDF from JSON Data
async function generatePdfFromJson(jsonPath) {
  const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

  // HTML template for the PDF report
  const htmlContent = `
    <html>
      <head>
        <title>Docker Scout CVE Report</title>
        <style>
          table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #f2f2f2; }
        </style>
      </head>
      <body>
        <h1>Docker Scout CVE Report</h1>
        <table>
          <thead>
            <tr>
              <th>CVE ID</th>
              <th>Severity</th>
              <th>Description</th>
              <th>Package</th>
            </tr>
          </thead>
          <tbody>
            ${jsonData
              .map(
                (entry) => `
                <tr>
                  <td>${entry.id}</td>
                  <td>${entry.severity}</td>
                  <td>${entry.description}</td>
                  <td>${entry.package}</td>
                </tr>`
              )
              .join('')}
          </tbody>
        </table>
      </body>
    </html>
  `;

  // Launch Puppeteer to generate the PDF
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(htmlContent, { waitUntil: 'load' });
  await page.pdf({ path: 'docker_scout_cve_report.pdf', format: 'A4' });

  console.log('PDF report generated: docker_scout_cve_report.pdf');
  await browser.close();
}

// Run the extraction and PDF generation steps
extractJsonFromZip(zipFilePath, extractedJsonPath);
generatePdfFromJson(extractedJsonPath).catch((err) => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
