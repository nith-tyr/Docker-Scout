const fs = require('fs');
const puppeteer = require('puppeteer');

// Function to generate HTML from CVE data
const generateCveHtmlReport = (cveData) => `
  <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
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
          ${cveData.map(cve => `
            <tr>
              <td>${cve.id}</td>
              <td>${cve.severity}</td>
              <td>${cve.description || 'N/A'}</td>
              <td>${cve.package || 'N/A'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </body>
  </html>
`;

(async () => {
  try {
    // Read the CVE data from scout-results.json
    const rawData = fs.readFileSync('sarif.result.json');
    const cveData = JSON.parse(rawData);

    const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();

    // Generate HTML content dynamically
    const htmlContent = generateCveHtmlReport(cveData);
    await page.setContent(htmlContent, { waitUntil: 'domcontentloaded' });

    // Generate PDF report
    await page.pdf({
      path: 'docker_scout_cve_report.pdf',
      format: 'A4',
      printBackground: true,
      margin: { top: '20px', bottom: '20px', left: '10px', right: '10px' },
    });

    console.log('PDF successfully generated: docker_scout_cve_report.pdf');
    await browser.close();
  } catch (error) {
    console.error('Error generating PDF:', error);
    process.exit(1);
  }
})();
