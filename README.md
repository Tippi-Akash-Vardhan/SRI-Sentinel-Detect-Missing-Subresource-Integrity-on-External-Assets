🔐 SRI Sentinel – Web Integrity Scanner

SRI Sentinel is a lightweight security tool that scans websites for missing Subresource Integrity (SRI) on externally loaded resources.

Missing SRI exposes websites to supply chain attacks, where compromised third-party scripts can inject malicious code.

⚡ Features
🔍 Detects external scripts, stylesheets, and fonts
🚨 Flags missing SRI attributes
🌐 Supports bulk domain scanning
🧹 Deduplicates findings
📄 Outputs clean JSON reports
⚡ Fast and simple to run
🛠️ How It Works

The tool:

Fetches a webpage
Parses HTML using BeautifulSoup
Identifies external resources
Checks for missing integrity attributes
Reports vulnerable assets
📦 Installation
pip install requests beautifulsoup4 urllib3
▶️ Usage
1. Add domains to domains.txt
example.com
google.com
2. Run the scanner
python sri_scanner.py
3. Output
sri_results.json
📊 Example Output
{
  "domain": "https://example.com",
  "status": "vulnerable",
  "sri_missing": [
    {
      "type": "script",
      "resource": "https://cdn.example.com/script.js"
    }
  ]
}
⚠️ Security Insight

Without SRI:

Third-party CDN compromise = full site compromise
No integrity validation on loaded scripts
Increased risk of Magecart-style attacks
🚧 Future Improvements
Multithreading for faster scanning
HTTP → HTTPS downgrade detection
Security headers analysis
CSV/HTML reporting
Integration with SecurityScorecard-style scoring
📜 License

MIT License
